import argparse
import os

def tree_view(start_path='files'):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

def create_note(note_name, folder):
    folder = os.path.join("files", folder)
    if not os.path.exists(folder) and folder != "files":
        os.makedirs(folder)
    file_path = os.path.join(folder, note_name + ".txt")
    with open(file_path, 'w') as f:
        f.write('')
    print(f"Note '{note_name}' created at '{file_path}'.")

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
    command_create = subparsers.add_parser('create', help='Create a plain note')
    command_create.add_argument('name', type=str, help='Name of the note to create')
    command_create.add_argument('--path','-p' ,type=str, default='files',
                                help='Directory folder (without file) to create the note in')

    # Subparser for encrypting files folder
    command_encrypt = subparsers.add_parser('encrypt', help='Encrypt notes folder with chosen method')
    command_encrypt.add_argument('--method', '-m', type=str, choices=['key', 'password'], default='key',
                                 help='Encryption method to use')

    # Subparser for decrypting files folder
    command_encrypt = subparsers.add_parser('decrypt', help='Decrypt notes folder with chosen method')
    command_encrypt.add_argument('--method', '-m', type=str, choices=['key', 'password'], default='key',
                                 help='Decryption method to use')


    args = parser.parse_args()
    if args.command == "create":
        create_note(args.name, args.path)
    elif args.command == "tree":
        tree_view()
    elif args.command == "encrypt":
        encrypt(args.method)
    elif args.command == "decrypt":
        decrypt(args.method)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()