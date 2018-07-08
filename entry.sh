#!/bin/sh

mongod --fork --syslog
gunicorn -w 2 -b 0.0.0.0:8000 app:app --log-file /dev/stderr --access-logfile /dev/stdout
