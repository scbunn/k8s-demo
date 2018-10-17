#!/usr/bin/env python
"""Demo API for Kubernetes.

Sample flask API to demonstrate kubernetes.  This application has a single
endpoint that returns the following::

    The hostname its runnings on
    The version
    The current timestamp
    The total # of times the endpoint has been hit.

The purpose of this application is to provide a simple, but non trivial
application that requires an external resource.

"""
import datetime
import os
import socket
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') or \
    'sqlite:////tmp/k8s.db'
db = SQLAlchemy(app)

version = os.environ.get('APP_VERSION', '1.0.0.dev')
hostname = socket.gethostname()

class PageTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Date, default=datetime.datetime.utcnow,
                       nullable=False,
                       unique=True)
    count = db.Column(db.Integer)

    def __str__(self):
        return f'PageTracker Hit Count {self.count}'

    def __repr__(self):
        return f'<PageTracker {self.count}>'


@app.route('/')
def index():
    p = PageTracker.query.filter_by(
        created=datetime.datetime.utcnow().strftime('%Y-%m-%d')).first()
    if not p:
        p = PageTracker(count=0)
    p.count += 1
    db.session.add(p)
    db.session.commit()
    return jsonify({
        'version': version,
        'server': hostname,
        'timestamp': datetime.datetime.utcnow(),
        'hit count': p.count
    }), 200


if __name__ == "__main__":
    db.create_all()
