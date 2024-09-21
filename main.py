from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import argparse
import shutil
import zipfile

# Shows the 'files' folder with a tree view
def tree(start_path='files'):
    has_content = False
    for root, dirs, files in os.walk(start_path):
        if root == start_path:
            if not dirs and not files:
                print("Nothing there")
                return
            for f in files:
                print(f"{f}")
            continue
        has_content = True
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level - 1)
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * level
        for f in files:
            print(f"{sub_indent}{f}")

    if not has_content:
        print("Nothing there")

# Zip a folder
def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

# Unzip a zip file
def unzip_folder(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_to)

# Creates a BNotes file
def mknote(directory):
    base_folder = os.path.abspath("files")
    full_path = os.path.abspath(os.path.join(base_folder, directory))
    folder = os.path.dirname(full_path)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if not full_path.endswith(".bn"):
        full_path += ".bn"

    with open(full_path, 'w') as f:
        f.write('')

    print(f"Note '{os.path.basename(full_path)}' created at '{full_path}'.")

# Creates a folder
def mkdir(directory):
    base_folder = os.path.abspath("files")
    full_path = os.path.abspath(os.path.join(base_folder, directory))

    if not full_path.startswith(base_folder):
        print("Error: Cannot create folders outside the 'files' folder.")
        return

    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Directory '{full_path}' created.")
    else:
        print(f"Directory '{full_path}' already exists.")

# Remove a file or directory
def rm(directories):
    base_folder = os.path.abspath("files")
    for directory in directories:
        directory = os.path.abspath(os.path.join(base_folder, directory))
        if not directory.startswith(base_folder):
            print(f"Error: Cannot remove '{directory}' outside the 'files' folder.")
            continue
        if os.path.isfile(directory):
            os.remove(directory)
            print(f"File '{directory}' removed.")
        elif os.path.isdir(directory):
            shutil.rmtree(directory)
            print(f"Directory '{directory}' and all its contents removed.")
        else:
            print(f"'{directory}' does not exist.")

# Generate a random 256-bit hexadecimal key
def genkey():
    key = os.urandom(32)
    print(f"Generated encryption key: {key.hex()}")

# AES Encryption
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as f:
        f.write(iv + encrypted_data)

    print(f"File '{file_path}' encrypted.")

# AES Decryption
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    with open(file_path, 'wb') as f:
        f.write(data)

    print(f"File '{file_path}' decrypted.")

def encrypt(key):
    zip_path = 'files.zip'
    encrypted_zip_path = 'files.zip.ebn'
    zip_folder('files', zip_path)
    encrypt_file(zip_path, key)
    os.rename(zip_path, encrypted_zip_path)
    shutil.rmtree('files')
    print(f"Encrypted file created: {encrypted_zip_path}")

def decrypt(key):
    encrypted_zip_path = 'files.zip.ebn'
    zip_path = 'files.zip'
    os.rename(encrypted_zip_path, zip_path)
    decrypt_file(zip_path, key)
    unzip_folder(zip_path, 'files')
    os.remove(zip_path)
    print(f"Decrypted files extracted to 'files' directory")

def main():
    # Main parser
    parser = argparse.ArgumentParser(description='This is BNotes CLI a notes app with encryption feature and much more!')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for displaying the folder structure
    command_tree = subparsers.add_parser('tree', help='Display the folder structure in a tree view')

    # Subparser for creating a note
    command_create = subparsers.add_parser('mknote', help='Create a plain note')
    command_create.add_argument('dir', type=str, help='Directory of the note to create (with the file name)')

    # Subparser for creating a folder
    command_create = subparsers.add_parser('mkdir', help='Create a folder')
    command_create.add_argument('dir', type=str, help='Directory of the folder to create (with the folder name)')

    # Subparser for removing a note or directory
    command_remove = subparsers.add_parser('rm', help='Remove a folder or a note')
    command_remove.add_argument('dirs', nargs='+', type=str, help='Directories to remove')

    # Subparser for encrypting files folder
    command_encrypt = subparsers.add_parser('encrypt', help='Encrypt notes folder with a provided key')
    command_encrypt.add_argument('key', type=str, help='Encryption key in hexadecimal format')

    # Subparser for decrypting files folder
    command_decrypt = subparsers.add_parser('decrypt', help='Decrypt notes folder with a provided key')
    command_decrypt.add_argument('key', type=str, help='Decryption key in hexadecimal format')

    # Subparser for generating an encryption key
    command_genkey = subparsers.add_parser('genkey', help='Generate a random encryption key')


    args = parser.parse_args()
    if args.command == "tree":
        tree()
    elif args.command == "mknote":
        mknote(args.dir)
    elif args.command == "mkdir":
        mkdir(args.dir)
    elif args.command == "rm":
        rm(args.dirs)
    elif args.command == "encrypt":
        key = bytes.fromhex(args.key)
        encrypt(key)
    elif args.command == "decrypt":
        key = bytes.fromhex(args.key)
        decrypt(key)
    elif args.command == "genkey":
        genkey()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()