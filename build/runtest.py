# File to do simple tests with our data, could update in the future
# for an actual interpreter for the DB

import sys
sys.path.append('classes')

from document import *

# for more commands, for now we can just add another elif and add
# code to test the command
if __name__ == '__main__':
    documents = {}
    while True:
        cmd = input('Do something: (c or u) ')
        if cmd == 'c':
            name = input('name is ?: ')
            data = {}

            print('Input keys and values (q to quit)')
            while True:
                key = input('key: ')
                value = input('value: ')
                if key == 'q' or value == 'q':
                    break
                data[key] = value

            d = Document(name, data)
            documents[name] = d
        elif cmd == 'u':
            name = input('name is ?: ')
            data = {}

            # right now this supports multiple entries poorly,
            # should update this to work better
            print('Input keys and values (q to quit)')
            while True:
                key = input('key: ')
                value = input('value: ')
                if key == 'q' or value == 'q':
                    break
                data[key] = value

            # right now we are locally retrieving documents, but in the
            # future we are going to want to get the document from storage
            documents[name].update(data)

        # if the user doesn't specify an actual command, we will just quit
        else:
            exit()
