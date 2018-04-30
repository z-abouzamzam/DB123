import os
import io
import json
import document

class Parser:
    """
    """

    def __init__():
        self.path = 'storage/'

    def parse(query):
        queryType = parse[0].lower()

        if queryType == 'select':
            return find(query[1:])
        elif queryType == 'update':
            return update(query[1:])
        elif queryType == 'delete':
            return delete(query[1:])
        else:
            print('Not a supported query type')

    def find(query):
        attributes = []
        fpath = path
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

        # for j in range(i, len(query), 3):
        #     conditions.append([query[j], query[j+1], query[j+2]])

        result = []

        print("[")

        if fpath == path:
            for file in os.listdir(fpath):
                values = document.read(file)
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

    def update():
        return

    def delete():
        return

