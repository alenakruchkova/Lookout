#!/usr/bin/env python

import argparse
import requests    # only recognizes url that start with http/https
import datetime
import time
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

####################################################

app = Flask(__name__)

# connection to the PostgreSQL database
db = SQLAlchemy()

####################################################

# setup command-line arg parsing
parser = argparse.ArgumentParser(description='Contacts a specified website at a specified interval to determine if the website is available.')
# add arguments
parser.add_argument("-u", "--url", type=str,
                     help="input url for the site to contact")
parser.add_argument("-d", "--database", type=str,
                     help="input database to record result to")
parser.add_argument("-i", "--interval", type=int, default=60.0,
                     help="input interval at which to contact specified site")
# parse arguments
args = parser.parse_args()


def get_status_code(host, interval):
    """ Retreives the status code of a website by requesting data from the host.

        If website does not exist, HTTP_status_code is assigned value 1000.
        If website is hanging, HTTP_status_code is assigned value 1002.
        If url can potentially result in a very large download,
        HTTP_status_code is assigned value 1001.
        If unexpected error is raised, HTTP_status_code is assigned value 1111.
        Records url, timestamp and status code to database.
    """

    url = host
    time_stamp = ('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

    # requests lib does not recognize url that do not start with http/https.
    # modify url if needed
    if not(host.startswith('http://') or host.startswith('https://')):
        host = "http://" + host

    try:
        r = requests.get(host, timeout=1, stream=True)
        # check if url could result in a very large download
        # assign HTTO_status_code 1001
        content = r.raw.read(100000+1, decode_content=True)
        if len(content) > 100000:
            HTTP_status_code = 1001
        else:
            HTTP_status_code = r.status_code
    # catch exception when iput website does not exist
    # assign HTTP_status_code 1000
    except requests.exceptions.ConnectionError:
        HTTP_status_code = 1000
    # catch exception when timeout is exceeded
    # assign HTTP_status_code 1002
    except requests.exceptions.ReadTimeout:
        HTTP_status_code = 1002
    # assign HTTP_status_code 1111 to all other errors
    except:
        print "Unexpected error:", sys.exc_info()[0]
        HTTP_status_code = 1111

    record = Record(HTTP_status_code=HTTP_status_code,
                    time_stamp=time_stamp,
                    url=url)

    #add to the session
    db.session.add(record)

    # commit
    db.session.commit()

    time.sleep(interval)

#####################################################

# model definitions

class Record(db.Model):
    """Records of site availability."""

    __tablename__ = "records"

    status_check_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    time_stamp = db.Column(db.String(22), nullable=False)
    HTTP_status_code = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(400), nullable=False)


# configure to use PstgreSQL database

app.config['SQLALCHEMY_DATABASE_URI'] = args.database
app.config['SQLALCHEMY_ECHO'] = False
db.app = app
db.init_app(app)

db.create_all()

#####################################################

if __name__ == '__main__':
    if not args.url or not args.database:
        print "error: too few arguments"
    else:
        while True:
            get_status_code(args.url, args.interval)
