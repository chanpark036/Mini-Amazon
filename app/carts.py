from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.cart import Cart
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('carts', __name__)

class submitOrderForm(FlaskForm):
    submit = SubmitField('Submit Order')
    
def getNumItems(productList):
    quantity = 0
    for prod in productList:
        quantity+=prod.quantity
    return quantity
def getTotalPrice(productList):
    price = 0
    for prod in productList:
        price+=(prod.u_price * prod.quantity)
    return price
    
@bp.route('/carts', methods = ['GET', 'POST'])
def carts():
    # get all available products for sale:
    #uid=keyboard input field
    
    form3 = submitOrderForm()
    uid = current_user.id
    products = Cart.get(uid)
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = form3)
    
@bp.route('/carts/<uid>,<pid>,<newValue>', methods = ['GET', 'POST'])
def changeCart(uid, pid, newValue):
    products = Cart.updateCount(uid, pid, newValue)
    
    submitForm = submitOrderForm()
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm)
    
@bp.route('/carts/<user_id>,<purchase_id>', methods=['GET','DELETE'])
def delete_product(user_id, purchase_id):
    products = Cart.delete_product(user_id, purchase_id)
    
    submitForm = submitOrderForm()
    return render_template('cart.html',
                           printprods = products, 
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm)
    
@bp.route('/submitOrder', methods = ['GET','POST','DELETE'])
def submitOrder():
    orderProducts = list(Cart.get(current_user.id))
    for prod in orderProducts:
        Inventory.decreaseInventory(prod.pid, prod.quantity)
    products = Cart.emptyCart(current_user.id)
    return render_template('submitPage.html',
                           orderInfo = orderProducts,
                           totalPrice = getTotalPrice(orderProducts))
    
