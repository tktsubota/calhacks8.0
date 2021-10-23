import functools
import json
import os

import json
import random
import string

import flask

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, request, Response, send_file
from flask_session import Session
from flask_compress import Compress
from flask_gzip import Gzip
import flask_login
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import ImmutableMultiDict

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import urllib.parse

from functools import wraps

from helpers import apology, usd, gen_random_string, gen_random_token, sendEmail

from cs50 import SQL

from datetime import datetime
from datetime import timedelta

import atexit
import time

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Only enable Flask debugging if an env var is set to true
app.debug = os.environ.get('FLASK_DEBUG') in ['true', 'True']

# Get app version from env
app_version = os.environ.get('APP_VERSION')

def is_logged_in() :
    return flask_login.current_user.is_authenticated

def getUserId() :

    if not is_logged_in() :
        return None
    return flask_login.current_user.id


@app.before_request
def before_request():

    if not request.path == "/redirectuser" and not request.path.startswith('/static') :
        cur_path = "/"
    if request.url.startswith('http://') and not "localhost" in request.url:
        # url = request.url.replace('http://', 'https://', 1)
        # code = 301
        # return redirect(url, code=code) 
        pass
    session.permanent = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_REFRESH_EACH_REQUEST"] = False

app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

# db = SQL("")

# " , logged_in = is_logged_in() "

Compress(app)
Gzip(app)
Session(app)

db = SQL("cockroachdb://adam:INszvx_c7RoH_dGI@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/slim-goat-4296.calhacks?sslmode=verify-full&sslrootcert=/Users/adam.manji/Library/CockroachCloud/certs/slim-goat-ca.crt")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(uid) :
    user = User()
    user.id = uid
    return user


@app.route("/", methods=["GET"])
def index():

    return render_template('index.html')


@app.route("/logout")
def logout() :
    flask_login.logout_user()
    return redirect("/")


@app.route('/login', methods=["GET", "POST"])
def login() :

    
    
    return render_template('login.html')


@app.route('/lessons')
def lessons() :

    pass


@app.route('/simulator')
def simulator() :

    pass


@app.route('/register', methods=["GET", "POST"])
def login() :

    if is_logged_in() :
        return redirect('/')

    if request.method == 'POST' :
        # confirm submission form
        email = request.form['email']
        password = request.form['password']

        # email verification token
        etoken = gen_random_token(6)

        # add user to db
        uid = gen_random_string(6)
        passhash = generate_password_hash(password)
        db.execute("INSERT INTO users (uid) VALUES (:u)", u=uid) # ADD OTHER VARIABLES TO THIS

        # send email to user w/ token
        tokenstring = 'Your verification token is: ' + etoken
        sendEmail(email, tokenstring, 'CalHacksApp Email Verification Token')

        # keep user cached w/ flask-login
        this_user = User()
        this_user.id = db.execute("SELECT uid FROM users WHERE email=:e", e=email)
        flask_login.login_user(this_user, remember=True)
    
    return render_template('register.html')


@app.route('/profile', methods=["GET", "POST"])
def profile() :

    # profile = db.execute("SELECT * FROM users WHERE uid=:u", u=getUserId())
    return 'put a profile page here bro'


@app.route('/search', methods=["GET", "POST"])
def search() :

    if request.method == "GET" :
        pass
    elif request.method == "POST" :
        pass

    return 'put a search page here bro'



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()