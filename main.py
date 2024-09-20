import argparse
import os

def create_note(note_name, folder):
    folder = os.path.join("files", folder)
    if not os.path.exists(folder) and folder != "files":
        os.makedirs(folder)
    file_path = os.path.join(folder, note_name + ".txt")
    with open(file_path, 'w') as f:
        f.write('')
    print(f"Note '{note_name}' created at '{file_path}'.")

def main():
    parser = argparse.ArgumentParser(description='This is BNotes CLI a notes app with encryption feature and much more!')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for creating a note
    command_create = subparsers.add_parser('create', help='Create a plain note')
    command_create.add_argument('name', type=str, help='Name of the note to create')
    command_create.add_argument('--path','-p' ,type=str, default='files', help='Directory folder (without file) to create the note in')

    args = parser.parse_args()

    if args.command == "create":
        create_note(args.name, args.path)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()