import os
import io
import json
import document

class Parser:
    '''
    Class for our parser, contains funcitons for the CRUD operations
    of our database.
    '''

    def __init__(self):
        self.path = 'storage/'

    def parse(self, query):
        '''
        General function to handle the different parsing operations.
        '''

        # first, we handle the query, selecting out the first word
        try:
            query = query.strip().split()
            queryType = query[0].lower()
        except IndexError:
            return

        # now, we have different cases for each test
        try:
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

        # invalid queries handled here
        except IndexError:
            print('Not a supported query type')

    def find(self, query):
        '''
        This function handles the logic for retrieval of information.
        The function is called when the user issues a SELECT command.
        The query argument is the remainder of the inputted query after the
        SELECT command.

        These queries are in the form:
        SELECT <attributes> FROM <document> WHERE <attribute = value>

        See README for more examples.
        '''

        # first we can initialize everything
        attributes = []
        fpath = self.path
        conditions = []

        # raise an exception, if the query is empty
        if(len(query) == 0):
            raise IndexError

        # get the document that we are selecting from, and the corresponding
        # attributes that we want to select
        for i in range(len(query)):
            if query[i].strip(',').lower() == '*':
                attributes.append('*')

            if query[i].strip(',').lower() != 'from':
                attributes.append(query[i].strip(','))

            elif query[i].strip(',').lower() == 'from':
                if query[i+1].lower() == '*':
                    i += 3
                    break
                else:
                    fpath += query[i+1]
                    i += 3
                    break
        # print(attributes)



        # here we have a specific document we are selecting from, so we try
        # to open it and get the attributes
        if fpath != self.path:
            try:
                doc = json.load(open(fpath + '.json'))
            except FileNotFoundError as e:
                print("Invalid Document name")
                return

            # check for if a document is a collection or not - note that we
            # haven't fully implemented collections yet so this check
            # currently doesn't do anything
            if 'collection' not in doc.keys() or doc['collection'] == '0':
                attr = {}

                # we go throught the remainder of the attributes
                for i in attributes:
                    # this case handles selecting documents from nested
                    # documents, these are in the form doc.attr
                    if '.' in i:
                        # we need to check if it's just a floating point number
                        # or actually a nested document
                        try:
                            float(i)
                        except ValueError:
                            # we can split the attributes and get the nested
                            # attributes
                            x = i.split('.')
                            try:
                                attr[i] = values[x[0]][x[1]]
                            except TypeError:
                                pass
                            except KeyError:
                                pass
                            continue

                    # if we wildcard selects, then we just get all the
                    # all the attributes from a document
                    if i == '*':
                        for j in doc.keys():
                            attr[j] = doc[j]
                    # otherwise, we actually have to check if the key value
                    # pair is in the document
                    else:
                        if i in doc.keys():
                            attr[i] = doc[i]

                # now check to see if where clause is met
                whereidx = -1
                try:
                    whereidx = query.index('where')
                    # print(whereidx)
                # if no where clause, we can simply print out our expression
                except ValueError:
                    try:
                        whereidx = query.index('WHERE')
                        # print(whereidx)
                    except ValueError:
                        print(str(attr))
                        return

                conditions = query[whereidx + 1:]
                # print(conditions)
                expression = ''

                # this uses the same logic as in delete to parse expressions
                for i in range(len(conditions)):
                    if i % 4 == 0:
                        flag = 0
                        try:
                            # Check if the value for the condition of deletion is a
                            # value which exists in the document, if not we know we
                            # are not deleting the document as part of the conditions
                            # cannot be met so we set our expression to False and move
                            # to the next document.
                            x = doc[conditions[i]]
                            if isinstance(x, str):
                                flag = 1
                                expression += '\'' + str(doc[conditions[i]]) + '\''
                            else:
                                expression += str(doc[conditions[i]])
                        except KeyError:
                            expression = 'False'
                            break
                    else:
                        # Translate regular equality to Python equality
                        if conditions[i] == '=':
                            expression += '=='
                        # As before if we are not looking at a comparison operator
                        elif (conditions[i] not in ['>', '<', '<=', '>=', 'and', 'or', '==', '!=']) and (flag == 1):
                            expression += '\'' + str(conditions[i]) + '\''
                        else:
                            expression += str(conditions[i])
                    expression += ' '
                try:
                    if eval(expression):
                        print(str(attr))
                except SyntaxError:
                    print('Invalid expression for document: ' + doc['documentName'])

                # now we can just print out the attributes that we have gotten
                # print(str(attr))
            elif doc['collection'] == '1':
                pass

        result = []

        # in this case, we have wildcarded the select clause, so we now need
        # to check the attributes for all the documents in our database
        if fpath == self.path:
            # we get the files in our directory, and load the documents
            for file in os.listdir(fpath):
                if file == '.DS_Store':
                    continue
                try:
                    values = json.load(open(fpath + file))
                except FileNotFoundError as e:
                    print("Invalid Document name")
                    return
                attr = {}

                # now, the remaining logic stays the same for getting
                # information from the documents
                for i in attributes:
                    # again, we have the check for a single nested document
                    if '.' in i:
                        # if it's a number do nothing
                        try:
                            float(i)
                        except ValueError:
                            x = i.split('.')
                            try:
                                attr[i] = values[x[0]][x[1]]
                            except TypeError:
                                pass
                            except KeyError:
                                pass
                            continue

                    # also have the wildcard check
                    if i == '*':
                        for j in values.keys():
                            attr[j] = values[j]
                    else:
                        if i in values.keys():
                            attr[i] = values[i]

                # same exact check as above to see if where clause is met
                # (I know, this can be much simpler, will update this repeated
                # code in the future, but for now, if it ain't broke, don't
                # fix it.)
                whereidx = -1
                try:
                    whereidx = query.index('where')
                    # print(whereidx)
                # if no where clause, we can simply print out our expression
                except ValueError:
                    try:
                        whereidx = query.index('WHERE')
                        # print(whereidx)
                    except ValueError:
                        if attr != {}:
                            print(values['documentName'] + " : " + str(attr))

                conditions = query[whereidx + 1:]
                # print(conditions)
                expression = ''

                # this uses the same logic as above to parse expressions
                for i in range(len(conditions)):
                    if i % 4 == 0:
                        flag = 0
                        try:
                            # Check if the value for the condition of deletion is a
                            # value which exists in the document, if not we know we
                            # are not deleting the document as part of the conditions
                            # cannot be met so we set our expression to False and move
                            # to the next document.
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
                        # Translate regular equality to Python equality
                        if conditions[i] == '=':
                            expression += '=='
                        # As before if we are not looking at a comparison operator
                        elif (conditions[i] not in ['>', '<', '<=', '>=', 'and', 'or', '==', '!=']) and (flag == 1):
                            expression += '\'' + str(conditions[i]) + '\''
                        else:
                            expression += str(conditions[i])
                    expression += ' '
                try:
                    if eval(expression):
                        # finally print the attributes for each document found
                        if attr != {}:
                            print(values['documentName'] + " : " + str(attr))
                except SyntaxError:
                    print('Invalid expression for document: ' + values['documentName'])
                except TypeError:
                    pass

        return

    def create(self, query):
        '''
        This function handles the logic for creation of documents.
        The function is called when the user issues a CREATE command.
        The query argument is the remainder of the inputted query after the
        CREATE command.

        These queries are in the form:
        CREATE <document> <attr1 : value1 , attr2 : value2 , ...>

        See README for more examples.
        '''

        docName = query[0]

        # Check if the document already exists, if it does, let the user know
        # and don't override the document
        try:
            s = json.load(open(self.path + docName + '.json'))
            print('Invalid query! Document ' + docName + ' already exists ')
            return
        except FileNotFoundError:
            pass

        # Here we will use a string to copy the relevant parts of the query for
        # updating the document into an object which will later be used as a
        # dictionary to modify values in the document
        expression = '{'
        for value in query[1:]:
            addComma = 0
            temp = value
            # If the value has a comma make a note of it but remove it for the
            # purposes of setting the values of the dictionary
            if ',' in temp:
                addComma = 1
                temp = value.strip(',')

            #
            if temp != ':':
                # Check if the value is a number or a string
                try:
                    float(temp)
                except ValueError:
                    # If we are dealing with a simple data type just add it to
                    # the string escaped to set the value to a string in the
                    # dictionary
                    if temp not in ['{', '}', '},', '[', ']', '],']:
                        temp = '\'' + temp + '\''
                    # Otherwise we just add the value to the string normally
                    else:
                        temp = ' ' + temp + ' '

            expression += temp + (addComma * ',')

        expression += '}'

        # Handle case of empty document
        if expression == '{}':
            expression = 'dict()'

        try:
            # Use eval to translate the updated fields into a Python object
            # then dict() to make it into a dictionary
            attributes = eval(expression)
            attributes = dict(attributes)
        except:
            print('Invalid expression! See guidelines for valid expression types')
            return

        s = document.Document(docName, attributes)



    def update(self, query):
        '''
        This function handles the logic for retrieval of information.
        The function is called when the user issues a UPDATE command.
        The query argument is the remainder of the inputted query after the
        UPDATE command.

        These queries are in the form:
        UPDATE <document> SET <attribute : value>

        See README for more examples.
        '''

        docName = query[0]

        fpath = self.path + docName + '.json'

        # Load in the document
        try:
            doc = json.load(open(fpath))
        except FileNotFoundError as e:
            print("Invalid Document name")
            return

        # Here we will use a string to copy the relevant parts of the query for
        # updating the document into an object which will later be used as a
        # dictionary to modify values in the document
        expression = '{'
        flag = 0
        for value in query[2:]:
            addComma = 0
            temp = value

            # If we are now checking what a value should be set to set the flag
            if temp == ':':
                flag = 1

            # As before, if we have a comma, make note of it and remove it for
            # the purposes of the dictionary
            if ',' in temp:
                addComma = 1
                temp = value.strip(',')
                flag = 0

            # If we have a value that references a field as part of what the
            # updated value should be (after the ':') then set the value to the
            # current value of the field in that document
            if flag and temp in doc.keys():
                temp = doc[temp]

            # If we are not looking at an arithmetic or grouping operator add the
            # value to the expression based on whether it is a string or a number
            if temp not in [':', '+', '-', '*', '/', '(', ')']:
                try:
                    float(temp)
                except ValueError:
                    temp = '\'' + temp + '\''

            expression += str(temp) + (addComma * ',')

        expression += '}'
        # print(expression)

        # Handle case of empty update
        if expression == '{}':
            expression = 'dict()'

        try:
            # Use eval to translate the updated fields into a Python object
            # then dict() to make it into a dictionary
            attributes = eval(expression)
            attributes = dict(attributes)
        except:
            print('Invalid expression! See guidelines for valid expression types')
            return

        # Update the values from the query in the document
        for key in attributes.keys():
            if(key == 'documentName'):
                continue
            if attributes[key] == "None":
                doc[key] = None
                continue
            doc[key] = attributes[key]
        # Save the new document, overwriting the previous version
        s = document.Document(doc['documentName'], doc)

    def delete(self, query):
        '''
        This function handles the logic for retrieval of information.
        The function is called when the user issues a DELETE command.
        The query argument is the remainder of the inputted query after the
        DELETE command.

        These queries are in the form:
        DELETE FROM <document> WHERE <attribute {comparison} value>

        See README for more examples.
        '''

        # delete from where syntax
        # or just delete document (DELETE a)

        docName = query[1]
        conditions = query[3:]
        fpath = self.path

        # Handle wildcard document name (delete from all documents) and when
        # a document is specified
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

            # Here we take a slightly different approach to constructing our expression,
            # we have conditions such as those of the form {field < value} so we
            # construct an expression that has the value of that field in the document
            # in place of the field name. If, for example we want to delete from documents
            # where {id < 5} we construct the expression as '[document id] < 5' so if all
            # conditions are met the entire expression evaluates to True so we DELETE
            # the document in question
            expression = ''
            for i in range(len(conditions)):
                if i % 4 == 0:
                    flag = 0
                    try:
                        # Check if the value for the condition of deletion is a
                        # value which exists in the document, if not we know we
                        # are not deleting the document as part of the conditions
                        # cannot be met so we set our expression to False and move
                        # to the next document.
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
                    # Translate regular equality to Python equality
                    if conditions[i] == '=':
                        expression += '=='
                    # As before if we are not looking at a comparison operator
                    elif (conditions[i] not in ['>', '<', '<=', '>=', 'and', 'or', '==', '!=']) and (flag == 1):
                        expression += '\'' + str(conditions[i]) + '\''
                    else:
                        expression += str(conditions[i])
                expression += ' '
            # print(expression)
            try:
                if eval(expression):
                    # print('removing')
                    os.remove(self.path + values['documentName'] + '.json')
            except SyntaxError:
                print('Invalid expression for document: ' + values['documentName'])
