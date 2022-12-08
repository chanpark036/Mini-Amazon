from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, seller, balance, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.seller = seller
        self.balance = balance
        self.address = address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, seller, balance, address
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, seller, balance, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, seller, balance, address)
VALUES(:email, :password, :firstname, :lastname, :seller, :balance, :address)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname,
                                  seller=seller, balance=balance,
                                  address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, seller, balance, address
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
    
    # update user email unless a user with that email already exists
    @staticmethod
    def update_email(id, email):
        try:
            rows = app.db.execute("""
    UPDATE Users
    SET email = :email
    WHERE id= :id
    """,
                                email=email,
                                id=id)
        except Exception as e:
            print(str(e))
            return None
  
    # update user password
    @staticmethod
    def update_password(id, password):
        rows = app.db.execute("""
UPDATE Users
SET password = :password
WHERE id= :id
""",
                              password=generate_password_hash(password),
                              id=id)
        
    # update user first name
    @staticmethod
    def update_firstname(id, firstname):
        rows = app.db.execute("""
UPDATE Users
SET firstname = :firstname 
WHERE id= :id
""",
                              firstname=firstname,
                              id=id)
        
    # update user last name
    @staticmethod
    def update_lastname(id, lastname):
        rows = app.db.execute("""
UPDATE Users
SET lastname = :lastname
WHERE id= :id
""",
                              lastname=lastname,
                              id=id)
        
    # update user address
    @staticmethod
    def update_address(id, address):
        rows = app.db.execute("""
UPDATE Users
SET address = :address
WHERE id= :id
""",
                              address=address,
                              id=id)
        
    # update user balance: users can either withdraw full balance or add to balance
    @staticmethod
    def update_balance(id, balance):
        rows = app.db.execute("""
UPDATE Users
SET balance = :balance
WHERE id= :id
""",
                              balance=balance,
                              id=id)


    '''
    *** change_balance(id, changeVal) takes a user's balance and updates their balance by a given amount.
    @param: id = unique user ID, changeVal = the amount to add or take away from a balance
    @return: none'''
    def change_balance(id, changeVal):
        rows = app.db.execute("""
            UPDATE Users
            SET balance = :balance
            WHERE id= :id
            """,
            balance=User.get(id).balance+float(changeVal),
            id=id)        
        