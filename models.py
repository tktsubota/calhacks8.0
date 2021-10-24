"""
Data model for Financial Literacy Web App

This provides the interface to the SQL database, allowing most app logic to be in pure Python.
"""

from enum import Enum
from cs50 import SQL
from helpers import lookup

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
        self.action = action
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

class Student:
    """A student, a user of the web app."""
    
    def __init__(self):
        self.uuid = 0
        self.current_lesson = 0
        self.lesson_progress = 0 # Not sure what data format this should be
        self.cash = 0

    def get_quantity(self, type, symbol):
        """Returns the quantity of a given SYMBOL of a given TYPE held by the student."""
        # SQL implementation
        return 10

    def get_value(self, type=None, symbol=None):
        """
        Returns the monetary value for the total amount of a given SYMBOL of a given TYPE held by the student.
        If SYMBOL is None, return the total value held for that entire TYPE.
        IF TYPE is also None, return the total account value held overall by the student. This includes cash.
        """
        # SQL implementation using Transactions table
        return 100

    def perform_transaction(self, transaction):
        """
        Perform transaction if valid, otherwise throw an exception. Must wrap in try/except to avoid crashing.
        
        Preconditions for buy: enough cash
        Preconditions for sell: student owns it
        """
        if transaction.action is Transaction.Action.BUY:
            if transaction.price * transaction.quantity > self.cash:
                raise Exception(f'Not enough cash to buy {transaction.quantity} shares of {transaction.name} at ${transaction.price:.2f}.')
        else:
            amount_to_sell = self.get_quantity(self, transaction.type, transaction.symbol)
            if amount_to_sell < transaction.quantity:
                raise Exception(f'Not enough shares of {transaction.name} to sell.')
            
        transaction.student = self

        # ADD TRANSACTION TO SQL TABLE
        db.execute("INSERT INTO transactions")

    def get_user_evaluation() :

        pass

    def get_portfolio(self, type) :
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

    def evaluate_portfolio(portfolio, type) :
        value = 0
        for e in portfolio :
            value += portfolio[e] * lookup(e)['price']
        return value