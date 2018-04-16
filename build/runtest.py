# File to do simple tests with our data, could update in the future
# for an actual interpreter for the DB

import sys
import os
sys.path.append('classes')

from document import *

# some helper functions
def readDoc(filename):
    doc = read(filename)
    # do some error check in document class
    return doc

def loadDocs():
    docs = {}
    if not os.path.exists('storage/'):
        print('error: no files exist')
        return

    for file in os.listdir('storage/'):
        filename = file[:-5]  # need to remove .json
        print(filename)
        docs[filename] = readDoc(filename)
    return docs


# for more commands, for now we can just add another elif and add
# code to test the command
if __name__ == '__main__':
    # loaddocs not quite working..
    documents = loadDocs()
    print(documents['new'])
    while True:
        cmd = input('Do something: (c or u) ')
        if cmd == 'c':
            name = input('name is ?: ')
            data = {}

            print('Input keys and values (q to quit)')
            while True:
                key = input('key: ')
                if key == 'q':
                    break
                value = input('value: ')
                if value == 'q':
                    break
                data[key] = value

            d = Document(name, data)
            documents[name] = d

        elif cmd == 'u':
            name = input('name is ?: ')
            if name not in documents.keys():
                print('Document not found!')
                continue
            data = {}

            # right now this supports multiple entries poorly,
            # should update this to work better
            print('Input keys and values (q to quit)')
            while True:
                key = input('key: ')
                if key == 'q':
                    break
                value = input('value: ')
                if value == 'q':
                    break
                data[key] = value

            # right now we are locally retrieving documents, but in the
            # future we are going to want to get the document from storage
            documents[name].update(data)
            print(documents[name])
        # if the user doesn't specify an actual command, we will just quit
        else:
            exit()
