from flask import Flask,request
from flask import Flask,render_template
from flask import jsonify
from flask import json
##from flask import Markup
import MySQLdb
import jinja2
import os
import boto

import csv
from datetime import datetime
import time
import random
import sys

## Python package to generate Random Names
import names

application = Flask(__name__)




@application.route('/parking')
# Configure the Jinja2 environment.
def main_main1():

    lat=37.7811378
    lon=-122.396479099999
    dist=0.0621371
    db = MySQLdb.connect(host='mjdbpyhoninstance.ccunictkoaw7.us-west-2.rds.amazonaws.com', port=3306, db='mjdbpython', user='mayank', passwd='mayank123')
    cursor = db.cursor()
    #query= 'select f_name from '+table_name+' where age between '+str(youngest_allowed)+' and '+str(oldest_allowed)+' AND income between '+str(poorest_allowed)+' and '+str(richest_allowed)+' and health_status="ALIVE"'
    query= 'select * from  parking_spots'

    q='SELECT *,(3959 * acos ( cos ( radians('+str(lat)+') ) * cos( radians( p_lat ) ) * cos( radians( p_long ) - radians('+') ) + sin ( radians('+str(lat)+') ) * sin( radians( p_lat ) ))) AS distance From parking_spots HAVING distance > '+str(dist)+' ORDER BY distance'

    print "Mj Here"
    #cursor.execute(query)
    cursor.execute(query)

    res=cursor.fetchall()
    print res#[0][0]

    user = {'nickname': 'Miguel'}  # fake user
    mj1=['MJ','Jain','PJ']
    return jsonify(mj1)



@application.route('/')
# Configure the Jinja2 environment.
def main_main():
    user = {'nickname': 'Miguel'}  # fake user
    mj1=['MJ','Jain','PJ']
    return render_template('index.html',
                           title='Home',
                           user=mj1)


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()