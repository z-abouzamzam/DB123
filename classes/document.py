import json
import io
import os

class Document:
    """
    """
    def __init__(self, name, attributes={}):

        attributes['documentName'] = name

        self.name = name
        self.filename = '../storage/' + name + '.json'
        self.attributes = attributes
        self.write()


    def write(self):
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str

        if not os.path.exists('../storage/'):
            os.makedirs('../storage/')

        with io.open(self.filename, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(self.attributes, indent=4, sort_keys=True,
                separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))

    def update(self, changes):
        for key, value in changes.items():
            self.attributes[key] = value
        self.write()

