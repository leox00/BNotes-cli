import argparse
import os

def create_note(note_name):
    with open(note_name, 'w') as f:
        f.write('')
    print(f"Note '{note_name}' created.")

def edit_note(note_name):
    pass

def main():
    parser = argparse.ArgumentParser(description='This is BNotes CLI a notes app with encryption feature and much more!')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for creating a note
    command_create = subparsers.add_parser('create', help='Create a plain note')
    command_create.add_argument('name', type=str, help='Name of the note to create')

    # Subparser for editing a note
    command_edit = subparsers.add_parser('edit', help='Edit a note')
    command_edit.add_argument('name', type=str, help='Name of the note to edit')

    args = parser.parse_args()

    if args.command == "create":
        create_note(args.name)
    elif args.command == "edit":
        edit_note(args.name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()