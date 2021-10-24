import os
import requests
import urllib.parse
import string
import random

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pyEX as p

from flask import redirect, render_template, request, session, url_for
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("/apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def gen_random_string(l) :

    characters = string.ascii_letters + '1234567890'
    return ''.join(random.choice(characters) for _ in range(l))

def gen_random_token(l) :

    characters = '1234567890'
    return ''.join(random.choice(characters) for _ in range(l))


def sendEmail(address, message, subject) :

    from_addr = 'thebestcalhack@gmail.com'
    pw = 'duolingo'

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(from_addr, pw)

    msg = MIMEMultipart() # create a message

    # setup the parameters of the message
    msg['From']=from_addr
    msg['To']=address
    msg['Subject']=subject

    # add in the message body
    msg.attach(MIMEText(message))

    # send the message via the server set up earlier.
    s.send_message(msg)

    del msg

    s.quit()


def lookup(symbol, crypto=False):
    """Look up quote for symbol."""

    symbol_original = symbol

    if crypto :
        symbol += 'USDT'

    # Contact API
    try:
        client = p.Client(api_token='pk_54e28984093d4115931ec8b87b421ae2', version='stable')
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = client.quote(symbol)
        if crypto:
            return {
                "name": cryptoname(symbol_original),
                "price": float(quote["latestPrice"]),
                "symbol": quote["symbol"]
            }
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None
    
def cryptoname(symbol):
    url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol='+symbol+'&market=CNY&apikey=9XEDKZ2RWDICFDG6'
    r = requests.get(url)
    data = r.json()
    return data['Meta Data']['3. Digital Currency Name']