#!/bin/env python
import os
from flask import Flask, render_template
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

@app.route('/greet/<username>')
def greet(username):
    db_conn = mysql.connect()
    cursor = db_conn.cursor()
    stmt = "SELECT visits FROM visitors WHERE visitor = '{0}'".format(username)
    cursor.execute(stmt)
    result = cursor.fetchone()
    print result
    if not result:
      stmt = "INSERT INTO visitors (visitor, visits) VALUES ('{0}',1)".format(username)
      cursor.execute(stmt)
      db_conn.commit()
      print "gnoe"
      visits = 1
    else:
      visits = result[0]
      stmt = "UPDATE visitors SET visits = visits + 1 WHERE visitor = '{0}'".format(username)
      cursor.execute(stmt)
      db_conn.commit()
    return render_template('greet.html', username=username, visits=visits)

def init_db():
    mysql.init_app(app)
    db_conn = mysql.connect()
    cursor = db_conn.cursor()
    stmt = "SHOW TABLES LIKE 'visitors'"
    cursor.execute(stmt)
    result = cursor.fetchall()
    if not result:
      tblsql = '''CREATE TABLE visitors (visitor VARCHAR(30) DEFAULT NULL, visits INTEGER DEFAULT 0);'''
      cursor.execute(tblsql)

def configure():
    appcfg = os.getenv('APPCFG')
    if appcfg is not None:
        app.config.from_envvar('APPCFG')

if __name__ == '__main__':
    configure()
    init_db()
    app.run(host='0.0.0.0', port=8080)
