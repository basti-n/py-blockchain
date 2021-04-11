import json
from os import read
import pickle
from typing import Union

# (1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.

STORAGE_FILE = 'assignment-store.txt'
STORAGE_FILE_PICKLE = 'assigment-store.p'


def get_storage_file(storage_type: 'json' or 'pickle') -> STORAGE_FILE or STORAGE_FILE_PICKLE:
    return STORAGE_FILE if storage_type == 'json' else STORAGE_FILE_PICKLE


def handle_binary_input(reply: str) -> bool:
    return any(match in reply.lower() for match in ['y', 'yes', '1'])


def ask_for_input() -> str:
    return input('What would you like to store? ')


def print_options(options=['For no input "NO"', 'For yes input "YES"'], *, showDivider: bool = False) -> None:
    for option in options:
        print(option)
        if(showDivider):
            print(20 * '-')


def ask_for_continue() -> bool:
    print_options(showDivider=True)

    reply = input('Continue Game? ')

    return handle_binary_input(reply)


def save_to_file(content: str, *, isBytes=False) -> None:
    mode = 'bw' if isBytes else 'w'
    with open(get_storage_file('pickle' if isBytes else 'json'), mode=mode) as file:
        file.write(content)
        if not isBytes:
            file.write('\n')


def ask_to_view_file() -> bool:
    print_options()

    reply = input('Would you like to view the file? ')

    return handle_binary_input(reply)


def get_read_file(file, *, useJsonParser=False, usePickle=False) -> any:
    return pickle.loads(file.read()) if usePickle else json.loads(
        file.read()) if useJsonParser else file.read()


def print_file(file=STORAGE_FILE, *, useJsonParser=False, usePickle=False) -> None:
    mode = 'rb' if usePickle else 'r'
    try:
        with open(file, mode=mode) as file:
            read_file = get_read_file(
                file, useJsonParser=useJsonParser, usePickle=usePickle)
            print(read_file)
    except Exception as err:
        print('Error reading file')
        print(err)


# (2) The user should be able to output the data stored in the file in the terminal.
# (3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.

exit_game = False
in_memory_store = []


def save_to_store(content: str, *, list=in_memory_store) -> list[str]:
    list.append(content)
    return list


def ask_for_storage_type() -> 'json' or 'pickle':
    print_options(['Option 1: json', 'Option 2: pickle'])
    reply = input('Which format would you like to use? ')

    return 'json' if reply.lower() == 'json' else 'pickle'


storage_type = ask_for_storage_type()

while not exit_game:
    in_memory_store = save_to_store(ask_for_input())
    exit_game = not ask_for_continue()

save_to_file(json.dumps(in_memory_store) if storage_type ==
             'json' else pickle.dumps(in_memory_store), isBytes=storage_type != 'json')
if ask_to_view_file():
    print_file(get_storage_file(storage_type), useJsonParser=storage_type == 'json',
               usePickle=storage_type != 'json')
print('...Exiting Game...')
