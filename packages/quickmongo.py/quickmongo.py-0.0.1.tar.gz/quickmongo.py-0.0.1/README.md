# QuickMongo.py

Simple wrapper for PyMongo written in python! This module is for those who don't know pymongo but want to use it but if you are using for a very large scale things i aka Science Spot will prefer you to use PyMongo or other Database because it might be slow but will not matter alot until you are doing multiple Operations with it!

# Quick Docs

## Installation

**In your terminal:**
```
pip install quickmongo.py
```

**In your python file:**
```py
from quickmongo import Database

# If you are using locally
db = Database('mongodb://localhost:27017/', 'local')

# if you are using 'mongodb+srv://' uri then you should do something like this
db = Database(mongoURL, clusterName)
# mongourl will be the 'mongodb+srv://' uri link
# clusterName will be the name of the mongoose cluster. Eg:- Cluster0
# Incase if you don't know what is your clustername you will get an TypeError with available clusters!
```

## Options of Databases

Set some options for your database as a dict which is optional

```py
options = {
    'collection_name': 'yourCollectionName' # Collection name will be 'python' as default
}

db = Database(mongoURL, clusterName, options)
# mongoURL and clusterName is described above
```

## Get databases and collections

```py
# Get all database names under the link
print(db.all_database_names())
# Check if the given database exists in the list
print(db.database_exists('Cluster0'))

# Get all collections names under the link
print(db.all_collection_names())
# Check if the given collection exists in the list
print(db.collection_exists('python'))
```

## All Operations

```py
db.set('foo', 'bar') # Will set value 'bar' for the key 'foo'
db.get('foo') # Will return 'bar' which is the value of the key 'foo'

db.all() # Will return all keys and values of the collection! {'key': 'foo', 'value': 'bar'} as a dict
db.startsWith('f') # Will sort all data whose keys startswith 'f' as {'key': 'foo', 'value': 'bar'}

db.delete('foo') # Will delete value of the key 'foo'
db.deleteAll() # Will delete all values of the all keys! Simple drop() function

db.set('foo', 1) # Simple set function given description above

db.add('foo', 2) # Will add 2 to the old value. So the current value will be 3
db.subtract('foo', 1) # Will subtract 1 from old value of the key 'foo'. So the current value will be 1

db.typeof('foo') # Its currently int so it will return <class 'int'>
```

> Currently this package is under developement! But still this package works very well!

# Support

- [Join our Discord Server](https://discord.gg/FrduEZd)
- [GitHub Repo](https://github.com/Scientific-Guy/quickmongo.py)