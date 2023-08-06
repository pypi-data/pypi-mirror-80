import dbm
import shelve
import pathlib

class EmbeddedCache:
    def __init__(self):
        # print('Which db: ', dbm.whichdb('./cache.db'))
        pass

    def insert(self, key, parent=None, data=None):
        if parent:
            key = '.'.join((parent, key))

        # with dbm.open('cache', 'c') as db:
        with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'c') as db:
            db[key] = data
            # assert db[key.encode('utf-8')] == data.encode('utf-8')
            # assert db[key] == data.encode('utf-8')

    def search(self, key, parent=None):
        if parent:
            key = '.'.join((parent, key))
        
        # with dbm.open('cache', 'r') as db:
        with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'r') as db:
            return db.get(key, None)

    def keys(self):
        # with dbm.open('cache', 'r') as db:
        with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'r') as db:
            return db.keys()

    def list_all(self):
        # with dbm.open('cache', 'r') as db:
        with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'r') as db:
            # print('All keys():', db.keys())
            return dict(map(lambda k: (k, db.get(k)), db.keys()))

    def delete(self, key, parent=None):
        if parent:
            key = '.'.join((parent, key))
        
        # with dbm.open('cache', 'w') as db:
        with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'w') as db:
            if db.get(key, None):
                del db[key]
            # print('Remaining keys():', db.keys())

    def clear(self):
        # with dbm.open('cache', 'w') as db:
        with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'w') as db:
            db.clear()
                # del db[key]

