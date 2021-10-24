"""
Data model for Financial Literacy Web App

This provides the interface to the SQL database, allowing most app logic to be in pure Python.
"""

from enum import Enum
from cs50 import SQL
from helpers import lookup, gen_random_string
from datetime import datetime

db = SQL("cockroachdb://adam:INszvx_c7RoH_dGI@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/slim-goat-4296.calhacks?sslmode=verify-full&sslrootcert=/Users/adam.manji/Library/CockroachCloud/certs/slim-goat-ca.crt")

class Transaction:
    """A buy or sell transaction"""

    class Action(Enum):
        """Action enum for buying vs. selling"""
        BUY = 0
        SELL = 1

    class Type(Enum):
        """Type enum for differentiating between different transaction types"""
        STOCK = 0
        FUND = 1
        CRYPTO = 2

    def __init__(self, action, type, symbol, price, quantity):
        self.type = type
        self.action = (action == 'buy')
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

class Student:
    """A student, a user of the web app."""
    
    def __init__(self, uid):
        self.uuid = uid
        self.current_lesson = 0
        self.lesson_progress = 0
        self.cash = 0

    def get_quantity(self, symbol):
        """Returns the quantity of a given SYMBOL of a given TYPE held by the student."""
        out = 0
        transactions = db.execute("SELECT quantity, buy FROM transactions WHERE uid=:u and symbol=:s", u=self.uuid, s=symbol)
        for t in transactions :
            if t['buy'] :
                out += t['quantity']
            else :
                out -= t['quantity']
        return out

    def get_value(self, type=None, symbol=None):
        """
        Returns the monetary value for the total amount of a given SYMBOL of a given TYPE held by the student.
        If SYMBOL is None, return the total value held for that entire TYPE.
        IF TYPE is also None, return the total account value held overall by the student. This includes cash.
        """
        if not symbol :

            pass

        elif not type :

            pass

        else :

            return self.get_user_evaluation()


    def perform_transaction(self, transaction):
        """
        Perform transaction if valid, otherwise throw an exception. Must wrap in try/except to avoid crashing.
        
        Preconditions for buy: enough cash
        Preconditions for sell: student owns it
        """

        self.cash = db.execute('SELECT cash FROM users WHERE uid=:u', u=self.uuid)[0]['cash']

        if transaction.action : # buying
            if transaction.price * float(transaction.quantity) > self.cash:
                raise Exception(f'Not enough cash to buy {transaction.quantity} shares of {transaction.symbol} at ${transaction.price:.2f}.')
        else:
            amount_to_sell = self.get_quantity(transaction.symbol)
            if amount_to_sell < transaction.quantity:
                raise Exception(f'Not enough shares of {transaction.name} to sell.')
            
        transaction.student = self

        # ADD TRANSACTION TO SQL TABLE
        count_transactions = db.execute("SELECT COUNT(1) FROM transactions")[0]['count']
        uid = self.uuid
        tid = gen_random_string(8)
        ts = datetime.now()
        db.execute("INSERT INTO transactions (pk, tid, uid, type, symbol, price, quantity, buy, ts) VALUES (:c, :t, :u, :ty, :s, :p, :q, :a, :time)", c=count_transactions, t=tid, u=uid, ty=transaction.type, s=transaction.symbol, p=transaction.price, q=transaction.quantity, a=transaction.action, time=ts)
        db.execute("COMMIT")

        # change student cash

        if transaction.action : # buying
            self.cash = self.cash - transaction.price * float(transaction.quantity)
        else :
            self.cash = self.cash + transaction.price * float(transaction.quantity)
        db.execute("UPDATE users SET cash=:c WHERE uid=:u", c=self.cash, u=uid)


    def get_user_evaluation(self) :

        cash = db.execute('SELECT cash FROM users WHERE uid=:u', u=self.uuid)[0]['cash']
        portfolio_val = Student.evaluate_portfolio(self.get_portfolio())
        return cash + portfolio_val

    def get_portfolio(self) :
        out = {}
        transactions = db.execute("SELECT * FROM transactions WHERE uid=:u", u=self.uuid)
        for t in transactions :
            val = 0
            if t['symbol'] in out :
                val = out['symbol']
            if t['buy'] :
                val += t['quantity']
            else :
                val -= t['quantity']
            out['symbol'] = val
        return out

    def evaluate_portfolio(portfolio) :
        value = 0
        for e in portfolio :
            value += portfolio[e] * lookup(e)['price']
        return value