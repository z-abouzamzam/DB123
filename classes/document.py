import json
import io

class Document:
    """
    """
    def __init__(self, name, attributes={}):
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str

        attributes['documentName'] = name
        filename = '../storage/' + name + '.json'

        with io.open(filename, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(attributes, indent=4, sort_keys=True,
                separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))
