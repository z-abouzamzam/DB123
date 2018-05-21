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
        try:
            query = query.strip().split()
            queryType = query[0].lower()
        except IndexError:
            return
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
            try:
                doc = json.load(open(fpath + '.json'))
            except FileNotFoundError as e:
                print("Invalid Document name")
                return

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
                if file == '.DS_Store':
                    continue
                try:
                    values = json.load(open(fpath + file))
                except FileNotFoundError as e:
                    print("Invalid Document name")
                    return
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

        # query in form ['document', 'a', ':', '5', 'b', '4', 'c', 'hello']

        # Constraints on expression:
        # only simple datatypes: string int float
        # need space between colon and key values
        # commas needed between multiple values

        # example CREATE d a : 45, c : 2.2, f : hello

        docName = query[0]

        expression = '{'

        for value in query[1:]:
            addComma = 0
            temp = value
            if ',' in temp:
                addComma = 1
                temp = value.strip(',')

            if temp != ':':
                try:
                    float(temp)
                except ValueError:
                    temp = '\'' + temp + '\''

            expression += temp + (addComma * ',')

        expression += '}'

        if expression == '{}':
            expression = 'dict()'

        try:
            attributes = eval(expression)
            attributes = dict(attributes)
        except:
            print('Invalid expression! See guidelines for valid expression types')
            return

        s = document.Document(docName, attributes)



    def update(self, query):
        # will look same as create, for now we will just delete old and create new
        # update document (a : 5, b : 6, c : hello)
        docName = query[0]

        fpath = self.path + docName + '.json'

        try:
            doc = json.load(open(fpath))
        except FileNotFoundError as e:
            print("Invalid Document name")
            return

        expression = '{'
        flag = 0
        for value in query[1:]:
            addComma = 0
            temp = value

            if temp == ':':
                flag = 1
            if ',' in temp:
                addComma = 1
                temp = value.strip(',')
                flag = 0

            if flag and temp in doc.keys():
                temp = doc[temp]

            if temp not in [':', '+', '-', '*', '/', '(', ')']:
                try:
                    float(temp)
                except ValueError:
                    temp = '\'' + temp + '\''

            expression += str(temp) + (addComma * ',')

        expression += '}'
        print(expression)

        if expression == '{}':
            expression = 'dict()'

        try:
            attributes = eval(expression)
            attributes = dict(attributes)
        except:
            print('Invalid expression! See guidelines for valid expression types')
            return

        for key in attributes.keys():
            if attributes[key] == "None":
                doc.pop(key)
                continue
            doc[key] = attributes[key]

        s = document.Document(docName, doc)

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
            if len(conditions) == 0:
                conditions = ['documentName', '=', docName]

        for file in files:
            try:
                values = json.load(open(fpath + file))
            except FileNotFoundError as e:
                print("Invalid Document name")
                return
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
