import json
import uuid
import pymongo
import sys
import datetime as dt
import os

def _is_debug():
  return os.environ.get('DEBUG')

class MongoDB:

  def __init__(self, **argv):
    db_uri    = argv.get('db_uri')
    db_name   = argv.get('db_name')
    coll_name = argv.get('coll_name')

    self.argv = argv

    if _is_debug():
      print "connecting {}".format(db_uri)
    client = pymongo.MongoClient(db_uri)
    db   = getattr(client, db_name)
    coll = getattr(db, coll_name)
    if _is_debug():
      print "db:{}, coll:{}".format(db, coll)

    self.client  = client
    self.coll    = coll
    self.db      = db


  def get(self, dict={}):
    return list(self.coll.find(dict, {'_id': False } ))

  def put(self, params):
    self.coll.insert_one(params)


if __name__ == '__main__':
  y = MongoDB(**{ "db_uri":"mongodb://localhost", "db_name": "test", "coll_name": "test_coll" })

  datetime_str = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
  y.put({ 'date' : datetime_str })
  data = y.get()
  print "\n".join([str(v) for v in data])


