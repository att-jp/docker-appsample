#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route,run,request,response,redirect,default_app,HTTPResponse
import requests
import datetime
import json
import os
import re
import copy

import shkawan_mongodb as shmongo

version_file = 'VERSION'
def _get_version():
  with open(version_file, "r") as f:
    version_string = f.readline().strip()
  return version_string

env = os.environ
version = _get_version()

db_argv = {
  "db_uri" : env.get('MONGODB_URI', 'mongodb://localhost'),
  "db_name": env.get('MONGODB_DB_NAME', 'test_db'),
  "coll_name": env.get('MONGODB_COLL_NAME', 'test_coll')
}

@route('/api', method='POST')
@route('/api/cl/<coll_name>', method='POST')
def _put(coll_name=None):
  response.content_type = 'application/json'
  put_db_argv = copy.deepcopy(db_argv)
  if coll_name:
    put_db_argv['coll_name'] = coll_name
  try:
    data = json.loads(request.body.read())
    shmongo.MongoDB(**put_db_argv).put(data)
  except Exception as e:
    return HTTPResponse(status=500, body="put ERROR({})".format(str(e)))
  return json.dumps( {} )

@route('/api', method='GET')
@route('/api/<name>', method='GET')
def _get(name=""):
  response.content_type = 'application/json'
  try:
    dict = {}
    if name:
      dict = { 'name':name }
    data = shmongo.MongoDB(**db_argv).get(dict)
  except Exception as e:
    return HTTPResponse(status=500, body="get ERROR({})".format(str(e)))
  return json.dumps( { "data" : data } )

@route('/env/<name>')
def _env(name):
  return env.get(name, "cannot get name:" + name)

@route('/hostname')
def _hostname():
  return os.uname()[1]

@route('/')
def _for_test():
  version = "00002"
  return "test ok({})\n".format(version)

@route('/version')
def _version():
  return "Version: {}".format(version)

app = default_app()

if __name__ == '__main__':
  port = env.get("APP_PORT", 9001)
  run(host='0.0.0.0', port=port, reloader=True, debug=True)

