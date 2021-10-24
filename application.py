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
from requests.api import get
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import ImmutableMultiDict

from models import Student, Transaction

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import urllib.parse

from functools import wraps

from helpers import apology, usd, gen_random_string, gen_random_token, sendEmail, lookup

from cs50 import SQL

import pyEX as p

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

# app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.secret_key = gen_random_string(32)

# db = SQL("")

# " , logged_in = is_logged_in() "

Compress(app)
Gzip(app)
Session(app)

db = SQL("cockroachdb://adam:INszvx_c7RoH_dGI@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/slim-goat-4296.calhacks?sslmode=verify-full&sslrootcert=/Users/troy/Library/CockroachCloud/certs/slim-goat-ca.crt")

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


@app.route('/simulator')
def simulator() :

    if not is_logged_in() :
        return redirect('/login')

    student = Student(getUserId())
    portfolio = student.get_portfolio_with_prices()
    stock = 0
    fund = 0
    crypto = 0
    for item in portfolio:
        amount = item['price'] * item['quantity']
        if item['type'] == 0:
            stock += amount
        elif item['type'] == 1:
            fund += amount
        else:
            crypto += amount
    return render_template('simulator.html', portfolio=portfolio, cash=student.cash, portfolio_value=student.evaluate_portfolio(student.get_portfolio()), progress=get_progress(), stock_value=stock, fund_value=fund, crypto_value=crypto)


@app.route('/history')
def history() :

    if not is_logged_in() :
        return redirect('/login')

    transactions = db.execute("SELECT * FROM transactions WHERE uid=:u", u=getUserId())

    return render_template('history.html', transactions=transactions, progress=get_progress())


@app.route("/logout")
def logout() :
    flask_login.logout_user()
    return redirect("/")


@app.route('/login', methods=["GET", "POST"])
def login() :

    if is_logged_in():
        return redirect('/lessons')

    if request.method == 'POST' :

        email = request.form['email']
        password = request.form['password']

        if not db.execute("SELECT COUNT(1) FROM users WHERE email=:e", e=email) :
            return render_template('login.html')

        info = db.execute("SELECT uid, password FROM users WHERE email=:e", e=request.form['email'])[0]
        if not check_password_hash(info['password'], password) :
            return render_template('login.html')

        this_user = User()
        this_user.id = info['uid']
        flask_login.login_user(this_user, remember=True)

        return redirect('/lessons')
    
    return render_template('login.html')


@app.route('/setprogress', methods=['POST'])
def setprogress() :
    try :
        lesson = request.method['lesson']
        activity = request.method['activity']
        progress = '{' + lesson + ', ' + activity + '}'
        db.execute("UPDATE users SET progress=:p WHERE uid=:u", p=progress, u=getUserId())
        try :
            db.execute("COMMIT")
        except :
            pass
        return {'error': 'none'}
    except Exception as e :
        return {'error': e}

@app.route('/addcash')
def addcash() :
    try :
        amount = int(request.form['amount'])
        cash = db.execute("SELECT cash FROM users WHERE uid=:u", u=getUserId()) + amount
        db.execute("UPDATE users SET cash=:c WHERE uid=:u", c=cash, u=getUserId())
        try :
            db.execute("COMMIT")
        except :
            pass
        return {'error': 'none'}
    except Exception as e :
        return {'error': e}

@app.route('/lessons')
def lessons() :

    if not is_logged_in() :

        return redirect('/login')

    return render_template('lessons.html', progress=get_progress())
    

# @app.route('/lesson/<n>')
def lesson(n) :

    if not is_logged_in() :

        return redirect('/login')

    return render_template('lesson.html', progress=get_progress(), n=int(n))

app.add_url_rule('/lesson/<n>', 'lesson', lesson)


@app.route('/buy', methods=['GET', 'POST'])
def buy() :

    if not is_logged_in() :
        return redirect('/login')

    if request.method == 'POST' :

        # takes symbol, quantity, type

        try :

            symbol = request.form['symbol']
            quantity = request.form['quantity']
            type = int(request.form['type'])
            if type == 2 :
                info = lookup(symbol, crypto=True)
            else :
                info = lookup(symbol)
            transaction = Transaction('buy', type, symbol, info['price'], quantity)
            student = Student(getUserId())
            student.perform_transaction(transaction)

            return render_template('buy.html', dialog='You have successfully purchased ' + quantity + ' shares of ' + info['name'])

        except Exception as e:
            return render_template('buy.html', dialog=f'An error occurred when performing your transaction: {e}', progress=get_progress())
    
    return render_template('buy.html', progress=get_progress())


@app.route('/sell', methods=['GET', 'POST'])
def sell() :

    if not is_logged_in() :
        return redirect('/login')

    if request.method == 'POST' :

        # takes symbol, quantity, type*

        #try :

        symbol = request.form['symbol']
        quantity = request.form['quantity']
        info = lookup(symbol)
        transaction = Transaction('sell', 0, symbol, info['price'], int(quantity))
        student = Student(getUserId())
        student.perform_transaction(transaction)

        return render_template('sell.html', dialog='You have successfully sold ' + quantity + ' shares of ' + info['name'], progress=get_progress())

        #except :

        #    return render_template('sell.html', dialog='An error occurred when performing your transaction')
    
    return render_template('sell.html', progress=get_progress())


@app.route('/register', methods=["GET", "POST"])
def register() :

    if is_logged_in() :
        return redirect('/lessons')

    if request.method == 'POST' :
        # confirm submission form
        email = request.form['email']
        password = request.form['password']

        # email verification token
        etoken = gen_random_token(6)

        # add user to db
        uid = gen_random_string(6)
        passhash = generate_password_hash(password)
        count_users = db.execute("SELECT COUNT(1) FROM users")[0]['count']
        db.execute("INSERT INTO users (pk, uid, email, password, token) VALUES (:c, :u, :e, :p, :t)", u=uid, e=email, p=passhash, t=etoken, c=count_users) # ADD OTHER VARIABLES TO THIS
        db.execute("COMMIT")

        # send email to user w/ token
        tokenstring = 'Your verification token is: ' + etoken
        # sendEmail(email, tokenstring, 'CalHacksApp Email Verification Token')

        # keep user cached w/ flask-login
        this_user = User()
        this_user.id = db.execute("SELECT uid FROM users WHERE email=:e", e=email)
        flask_login.login_user(this_user, remember=True)

        return redirect('/lessons')
    
    return render_template('register.html')


@app.route('/profile', methods=["GET", "POST"])
def profile() :

    # profile = db.execute("SELECT * FROM users WHERE uid=:u", u=getUserId())
    return 'put a profile page here bro'


@app.route('/search', methods=["GET", "POST"])
def search() :

    if not is_logged_in() :
        return redirect('/lessons')

    if request.method == "POST" :
        symbol = request.method['symbol']
        client = p.Client(api_token='pk_54e28984093d4115931ec8b87b421ae2', version='stable')
        info = client.quote(symbol)
        return render_template('search.html', progress=get_progress(), info=info)

    return render_template('search.html', progress=get_progress())


def get_progress() :

    if not is_logged_in() :
        return None
    
    return db.execute("SELECT progress FROM users WHERE uid=:u", u=getUserId())[0]["progress"]


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
