import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
token = os.environ['MONGOTOKEN']

class DiaryDB(object):

    client = MongoClient(token)

    dbm = client.tempUsers
    collection = dbm.AIO
    posts = dbm.posts
    backup = dbm.Backup

    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load()

    def load(self):
        t = self.posts.find_one()
        self.db = {} if t is None else t
        return True

    def dumpdb(self):
        self.backup.update_one({'_id': self.db['_id']}, {'$set' : self.db}, upsert=True)
        # self.posts.drop()
        self.posts.update_one({'_id': self.db['_id']}, {'$set' : self.db}, upsert=True)
        # post_id1 = self.posts.insert_one(self.db).inserted_id
        return True

    def set(self, key, value):
        try:
            self.db[str(key)] = value
            self.dumpdb()
        except Exception as e:
            print(f"[X] Error Saving Values to Database : {str(e)}")
            return False

    def sets(self, key, value):
        try:
            self.db[str(key)] = value
        except Exception as e:
            print(f"[X] Error Saving Values to Database : {str(e)}")
            return False

    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            # print("No Value Can Be Found for " + str(key))
            return False

    def delete(self, key):
        if key not in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True

    def resetdb(self):
        self.dbm.drop_collection(self.collection)
        return True
    
    
class BooksDB(object):
    client = MongoClient(token)
    db = client.books
    collection = db['9th_klass']
    
    def add(self, subject_name, nonfileurl, url):
        post = {'subject_name': subject_name,
                'nonfileurl' : nonfileurl,
                'url': url}
        posts = self.db.posts
        posts_id = posts.insert_one(post).inserted_id
    
    def get(self, subject_name):
        posts = self.db.posts
        post = posts.find_one({'subject_name': subject_name})
        return post if post else -1
        