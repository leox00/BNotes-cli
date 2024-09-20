import os
import argparse
import shutil

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

def encrypt(method):
    if method == 'key':
        print("Encrypt using key...")
    elif method == 'password':
        print("Encrypt using password...")
    else:
        print("Unknown encryption method.")

def decrypt(method):
    if method == 'key':
        print("Decrypt using key...")
    elif method == 'password':
        print("Decrypt using password...")
    else:
        print("Unknown decryption method.")

def main():
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
    command_encrypt = subparsers.add_parser('encrypt', help='Encrypt notes folder with chosen method')
    command_encrypt.add_argument('--method', '-m', type=str, choices=['key', 'password'], default='key',
                                 help='Encryption method to use')

    # Subparser for decrypting files folder
    command_encrypt = subparsers.add_parser('decrypt', help='Decrypt notes folder with chosen method')
    command_encrypt.add_argument('--method', '-m', type=str, choices=['key', 'password'], default='key',
                                 help='Decryption method to use')


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
        encrypt(args.method)
    elif args.command == "decrypt":
        decrypt(args.method)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()