import os
import io
import json
import document

class Parser:
    """
    """

    def __init__(self):
        self.path = 'storage/'

    def parse(self, query):
        query = query.strip().split()
        queryType = query[0].lower()

        if queryType == 'select':
            return self.find(query[1:])
        elif queryType == 'update':
            return self.update(query[1:])
        elif queryType == 'delete':
            return self.delete(query[1:])
        else:
            print('Not a supported query type')

    def find(self, query):
        attributes = []
        fpath = self.path
        conditions = []
        for i in range(len(query)):
            if query[i].lower() == '*':
                attributes.append('*')

            if query[i].lower() != 'from':
                attributes.append(query[i])

            elif query[i].lower() == 'from':
                if query[i+1].lower() == '*':
                    i += 3
                    break
                else:
                    fpath += query[i+1]
                    i += 3
                    break

        if fpath != self.path:
            doc = json.load(open(fpath))
            if doc['collection'] == '0':
                attr = {}
                for i in attributes:
                    if i == '*':
                        for j in doc.keys():
                            attr[j] = doc[j]
                    else:
                        if i in doc.keys():
                            attr[i] = doc[i]
                print(str(attr))
            elif doc['collection'] == '1':
                pass



        # for j in range(i, len(query), 3):
        #     conditions.append([query[j], query[j+1], query[j+2]])

        result = []

        print("[")

        if fpath == self.path:
            for file in os.listdir(fpath):
                values = json.load(open(fpath + file))
                attr = {}
                for i in attributes:
                    if i == '*':
                        for j in values.keys():
                            attr[j] = values[j]
                    else:
                        if i in values.keys():
                            attr[i] = values[i]
                if attr != {}:
                    print(values['documentName'] + " : " + str(attr))
        # else:
        #     pass

        print("]")

        return

    def update(self, query):
        return

    def delete(self, query):
        return

for file in os.listdir('storage/'):
    test = json.load(open('storage/'+file))
    attr = ['documentName']
    for i in attr:
        print i in test.keys()







