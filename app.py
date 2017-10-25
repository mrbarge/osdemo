#!/bin/env python
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/greet/<username>')
def greet(username):
    return render_template('greet.html', username=username)

def configure():
    appcfg = os.getenv('APPCFG')
    if appcfg is not None:
        app.config.from_envvar('APPCFG')

if __name__ == '__main__':
    configure()
    app.run(host='0.0.0.0')
