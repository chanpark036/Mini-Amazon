from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('carts', __name__)

class enterID(FlaskForm):
    uid = IntegerField('User ID')
    search = SubmitField('Search')

class updateData(FlaskForm):
    pid = IntegerField('ProductID')
    quantity = IntegerField('Number to Purchase')
    updateCart = SubmitField('Update Cart')
class submitOrderForm(FlaskForm):
    submit = SubmitField('Submit Order')
    
@bp.route('/carts', methods = ['GET', 'POST'])
def carts():
    # get all available products for sale:
    #uid=keyboard input field
    form1 = enterID()
    form2 = updateData()
    form3 = submitOrderForm()
    uid = form1.uid.data
    products = Cart.get(uid)
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           form1 = form1, 
                           form2 = form2, 
                           form3 = form3)
    
@bp.route('/carts/<uid>,<pid>,<newValue>', methods = ['GET', 'POST'])
def changeCart(uid, pid, newValue):
    products = Cart.updateCount(uid, pid, newValue)
    searchForm = enterID()
    updateForm = updateData()
    submitForm = submitOrderForm()
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           form1 = searchForm,
                           form2 = updateForm,
                           form3 = submitForm)
    
@bp.route('/carts/<user_id>,<purchase_id>', methods=['GET','DELETE'])
def delete_product(user_id, purchase_id):
    products = Cart.delete_product(user_id, purchase_id)
    searchForm = enterID()
    updateForm = updateData()
    submitForm = submitOrderForm()
    return render_template('cart.html',
                           printprods = products,
                           form1 = searchForm,
                           form2 = updateForm,
                           form3 = submitForm)
    
@bp.route('/submitOrder', methods = ['GET','POST'])
def submitOrder():
    return render_template('submitPage.html')
