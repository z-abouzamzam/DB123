# DB123

This is DB123, a document oriented database written in Python 3. The goal of
this project was to create a document oriented database using familiar SQL
syntax for queries. Enjoy!

Created by Zafir Abou-Zamzam and Roberto Mercado.

## Running the Database
This is pretty straightforward. Download the zip to your computer. Open a
terminal window from the DB123 directory. Now from this directory, run the
command `python classes/testing.py`. This requires Python 3 to run. A storage
folder will be created, and make sure you are always in this directory when
running the database.

## Command Types
Currently, we have support for all CRUD operations, some nested document logic,
and comparisons for various query types.
A general note for the expressions: Our parser is not the most sophisticated,
so be sure to follow the syntax **exactly** as it is listed here, or else your
queries may be unsuccessful.

Notes to keep in mind. Strings do not go in quotes, and in general, there should
be spaces between all symbols except commas. This is especially important for
nested documents and attributes which correspond to dictionaries or lists. For
example an attribute a corresponding to a dictionary and an attribute b corresponding
to a list should be formatted as such:

`CREATE document a : { b : 1, d : five }, b : [ 0, 1, 2, 3 ]`


### Creation
Commands here are in the form `CREATE <documentName> <attr1 : val1, attr2 : val2>`.
All attributes should be in the form `attrName : attrValue`. The database
supports primitive types (int, float, char), as well as more advanced datatypes
(string, array, document) for creation of attributes. All documents are stored
as json files in the storage directory. Once created, an attribute documentName
is automatically added to the document.

An example creation will be as follows, which creates a document titled document
with attributes a, b, and nestedDoc:

`CREATE document a : 5, b : 5.5, nestedDoc : { c : hello }`

### Retrieval
Commands here are in the form `SELECT <attribute1 , attribute2 , ...>
FROM <documentName> WHERE <expressions>`

**Wildcarded queries:** We can wildcard our retrievals for all documents, or for
all attributes in a specific set of documents, using the * symbol. To select
all attributes from all documents in our database, the following 2 queries
are equivalent:

`SELECT *` or `SELECT * FROM *`

To select all attributes from a single document, we can use the following:

`SELECT * FROM <documentName>`

Note that wildcards can be extended with WHERE clauses,


**Nested documents:** Note, these are in beta mode. We can select attributes
from nested documents directly by using a dot syntax. Example: if document
parent has a nested document child, and child has an attribute labeled 'a',
we can select it as follows (This only works for a single nested document):

`SELECT child.a from parent`

Example: To select attributes a, b, and c from a document called doc, where we
only want the values where a is greater than 5, we have the following command:

`SELECT a, b, c FROM doc WHERE a > 5`


### Update
Commands here are in the form `UPDATE <documentName> SET <attr1 : val1, attr2 : val 2>`
There should be spaces surrounding all operators, whether grouping or arithmetic.

Our database does not support true deletion of a single attribute. Instead, if
we would like to delete the value a specific attribute, we can set the value
to None. For example, if we want to "delete" attribute a from document d, we
can use an update as follows:

`UPDATE d SET a : None`


Example: To set the attributes a, b, and c of a document called 'doc1' to values
5, 'red', and the current c plus 23.50, respectively we have the following
command:

`UPDATE doc1 SET a : 5, b : red, c : c + 23.50`

### Deletion
Commands here are in the form `DELETE FROM <documentName> WHERE <condition1, condition2>`
Deletions in our database delete entire documents. If you would like to remove
a single key, value pair from a document, see the UPDATE section.

Simple example: To delete a single document titled h, we can do:

`DELETE FROM h`

Example: To delete all documents which have an attribute a equal to 10 or b less
than 15 we have the following command:

`DELETE FROM * WHERE a = 10 OR b < 15`
