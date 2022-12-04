from flask import render_template, redirect, url_for, Markup
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.cart import Cart
from .models.inventory import Inventory
from .models.purchase import Purchase
from .models.user import User


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
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form3 = submitOrderForm()
    uid = current_user.id
    products = Cart.get(uid)
    x = datetime.datetime.now()
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = form3,
                           time = x)
    
@bp.route('/carts/<uid>,<pid>,<newValue>', methods = ['GET', 'POST'])
def changeCart(uid, pid, newValue):
    products = Cart.updateCount(uid, pid, newValue)
    
    submitForm = submitOrderForm()
    x = datetime.datetime.now()
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm,
                           time = x)
    
@bp.route('/carts/<user_id>,<purchase_id>', methods=['GET','DELETE'])
def delete_product(user_id, purchase_id):
    products = Cart.delete_product(user_id, purchase_id)
    
    submitForm = submitOrderForm()
    x = datetime.datetime.now()
    return render_template('cart.html',
                           printprods = products, 
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm, time = x)
    
@bp.route('/submitOrder/<user_id>,<time>', methods = ['GET','POST','DELETE'])
def submitOrder(user_id, time):
    #decrease inventory
    form3 = submitOrderForm()
    orderProducts = list(Cart.get(current_user.id))
    for prod in orderProducts:
        availableQuant = Inventory.get_from_pid_specific(prod.pid, prod.sid).quantity
        if prod.quantity>availableQuant:
            message = "Your seller does not have enough inventory. Please adjust your order." + str(prod.sid) + str(prod.u_price)
            return render_template('cart.html',
                           printprods = orderProducts,
                           numItems = getNumItems(orderProducts),
                           totalPrice = getTotalPrice(orderProducts),form3=form3,
                           time = time, message=message)
    for prod in orderProducts:
        Inventory.decreaseInventory(prod.pid, prod.quantity, prod.sid)
        User.change_balance(prod.sid, prod.quantity*prod.u_price)
    #decrease buyer balance
    curr_balance = current_user.balance
    cost = getTotalPrice(orderProducts)
    new_balance = curr_balance - cost
    if new_balance>=0:
        User.update_balance(current_user.id, new_balance)
    else:
        message = "Insufficient funds. Please add funds to your account."
        return render_template('cart.html',
                           printprods = orderProducts,
                           numItems = getNumItems(orderProducts),
                           totalPrice = getTotalPrice(orderProducts),form3=form3,
                           time = time, message=message)
    #write order to purchase history
    purchase_id = Purchase.get_most_recent_purchase_id() + 1
    for prod in orderProducts:
        seller_id = prod.sid
        Purchase.add_purchase_history(purchase_id, current_user.id, seller_id, prod.pid, prod.quantity, time)
        purchase_id+=1
    #empty cart
    Cart.emptyCart(current_user.id)
    allProds = Purchase.get_detailed_order_page(current_user.id, time)
    for prod in allProds:
        print(prod.total_price)
    return render_template('submitPage.html',
                           orderInfo = allProds,
                           totalPrice = cost,
                           time = time)
    
