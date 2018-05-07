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
        elif queryType == 'create':
            return self.create(query[1:])
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
            doc = json.load(open(fpath + '.json'))
            if 'collection' not in doc.keys() or doc['collection'] == '0':
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

        # print("[")

        # need to do file not found errors

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

        # print("]")

        return

    def create(self, query):
        # document (int a 5, float b 4, c hello, int d, e)  - default to empty
        # string, always need a value

        # no empty fields

        # all special chars we parse as string
        # working on parsing

        # query in form ['document', '(a', '5,', 'b', '4,', 'c', 'hello)']
        docName = query[0]

        i = 1
        while(query[i + 1][-1] != ')'):
            key = query[i]
            try:
                float(query[i + 1][:-1])
            except ValueError:
                pass
            value = query[i + 1][:-1]



    def update(self, query):
        # will look same as create, for now we will just delete old and create new
        # update document (a 5, b 6, c hello)
        docName = query[0]

        fpath = self.path + docName

        return

    def delete(self, query):
        # delete from where syntax
        # or just delete document (DELETE a)

        docName = query[1]
        conditions = query[3:]
        fpath = self.path

        if docName == '*':
            files = os.listdir(fpath)

        else:
            files = [docName + '.json']

        print(files)

        for file in files:
            values = json.load(open(fpath + file))
            expression = ''
            for i in range(len(conditions)):
                if i % 4 == 0:
                    flag = 0
                    try:
                        x = values[conditions[i]]
                        if isinstance(x, str):
                            flag = 1
                            expression += '\'' + str(values[conditions[i]]) + '\''
                        else:
                            expression += str(values[conditions[i]])
                    except KeyError:
                        expression = 'False'
                        break
                else:
                    if conditions[i] == '=':
                        expression += '=='
                    elif (conditions[i] not in ['>', '<', '<=', '>=', 'and', 'or', '==', '!=']) and (flag == 1):
                        expression += '\'' + str(conditions[i]) + '\''
                    else:
                        expression += str(conditions[i])
                expression += ' '
            print(expression)
            try:
                if eval(expression):
                    print('removing')
                    os.remove(self.path + values['documentName'] + '.json')
            except SyntaxError:
                print('Invalid expression for document: ' + values['documentName'])
