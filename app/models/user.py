from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    '''
    User class represents a user object. A new user object is made when a new user registers for an account.
    User objects store the following information: user ID, email, first name, last name, their seller status,
    current balance, and address. 
    '''
    def __init__(self, id, email, firstname, lastname, seller, balance, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.seller = seller
        self.balance = balance
        self.address = address

    '''
    *** get_by_auth(email, password) takes an email and password and logs a user in if their information is correct.
    @param: email = unique user email, password = user's password
    @return: User to log the user in
    '''
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

    '''
    *** email_exists(email) takes an email and returns whether an account already exists with that email.
    If the length is greater than 0, an account exists with that email. If not, the email does not exist with an account. 
    @param: email = user email
    @return: True or False
    '''
    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    '''
    *** register(email, password, firstname, lastname, seller, balance, address) registers a user for a new account. 
    @param: email = unique user email, password = user's password, firstname = user's first name, lastname = user's last name,
    seller = user's seller status, balance = 0 by default, address = user's address
    @return: User if successfully registered
    '''
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

    '''
    *** get(uid) takes a user ID and returns all purchases associated with that user.
    @param: uid = unique user ID
    @return: uid, email, firstname, lastname, seller, balance, address
    '''
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
    
    '''
    *** update_email(id, email) takes a user ID and email and updates the user's email unless a user with that email already exists.
    @param: uid = unique user ID, email = desired new email
    @return: None
    '''
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
  
    '''
    *** update_password(id, password) takes a user ID and email and updates the user's password unless 
    they enter their password in twice and the passwords do not match.
    @param: uid = unique user ID, password = desired new password
    @return: None
    '''
    @staticmethod
    def update_password(id, password):
        rows = app.db.execute("""
UPDATE Users
SET password = :password
WHERE id= :id
""",
                              password=generate_password_hash(password),
                              id=id)
        
    '''
    *** update_firstname(id, firstname) takes a user ID and firstname and updates the user's first name.
    @param: uid = unique user ID, firstname = user's first name
    @return: None
    '''
    @staticmethod
    def update_firstname(id, firstname):
        rows = app.db.execute("""
UPDATE Users
SET firstname = :firstname 
WHERE id= :id
""",
                              firstname=firstname,
                              id=id)
        
    '''
    *** update_lastname(id, lastname) takes a user ID and lastname and updates the user's last name.
    @param: uid = unique user ID, lastname = user's last name
    @return: None
    '''
    @staticmethod
    def update_lastname(id, lastname):
        rows = app.db.execute("""
UPDATE Users
SET lastname = :lastname
WHERE id= :id
""",
                              lastname=lastname,
                              id=id)
    
    '''
    *** update_address(id, address) takes a user ID and address and updates the user's address.
    @param: uid = unique user ID, address = user's updated address
    @return: None
    '''   
    @staticmethod
    def update_address(id, address):
        rows = app.db.execute("""
UPDATE Users
SET address = :address
WHERE id= :id
""",
                              address=address,
                              id=id)
        
    '''
    *** update_balance(id, balance) takes a user ID and address and updates the user's balance.
    @param: uid = unique user ID, balance = user's new balance
    @return: None
    '''
    @staticmethod
    def update_balance(id, balance):
        rows = app.db.execute("""
UPDATE Users
SET balance = :balance
WHERE id= :id
""",
                              balance=balance,
                              id=id)    
        