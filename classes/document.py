import json
import io
import os

class Document:
    """
    The Document class is the basis for all data storage in the database.
    Creating a document accepts a name and optionally a dictionary of
    attributes and values and stores this data in a JSON object.
    """
    def __init__(self, name, attributes={}):

        attributes['documentName'] = name

        self.name = name
        self.filename = 'storage/' + name + '.json'
        self.attributes = attributes
        self.write()


    def write(self):
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str

        if not os.path.exists('storage/'):
            os.makedirs('storage/')

        with io.open(self.filename, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(self.attributes, indent=4, sort_keys=True,
                separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))

    def update(self, changes):
        for key, value in changes.items():
            self.attributes[key] = value
        self.write()



def read(filename):
    with open('storage/' + filename + '.json') as data_file:
        loaded = json.load(data_file)
    return loaded

def delete(filename):
    os.remove('storage/' + filename + '.json')
