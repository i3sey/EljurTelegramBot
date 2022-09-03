import os

from pymongo import MongoClient

try:
    from config import MONGOTOKEN
except Exception:
    token = os.environ['MONGOTOKEN']
else:
    token = MONGOTOKEN


class DiaryDB(object):
    
    client = MongoClient(token)

    dbm = client.tempUsers
    collection = dbm.AIO
    posts = dbm.posts

    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load()

    def load(self):
        t = self.posts.find_one()
        if t == None:
            self.db = {}
        else:
            self.db = t
        return True

    def dumpdb(self):
        try:
            post_id = self.posts.insert_one(self.db).inserted_id
            return True
        except:
            return False

    def set(self, key, value):
        try:
            self.db[str(key)] = value
            self.dumpdb()
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False

    def sets(self, key, value):
        try:
            self.db[str(key)] = value
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False

    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            # print("No Value Can Be Found for " + str(key))
            return False

    def delete(self, key):
        if not key in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True

    def resetdb(self):
        self.db = {}
        self.dumpdb()
        return True
