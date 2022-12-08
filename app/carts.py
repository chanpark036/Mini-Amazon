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

'''
*** getNumItems(productList) sums the quantity for all products in a product list.
    @param: productList = list of products of interest
    @return: quantity
'''   
def getNumItems(productList):
    quantity = 0
    for prod in productList:
        quantity+=prod.quantity
    return quantity

'''
*** getTotalPrice(productList) sums the price for all products in a product list.
    @param: productList = list of products of interest
    @return: price
'''  
def getTotalPrice(productList):
    price = 0
    for prod in productList:
        price+=(prod.u_price * prod.quantity)
    return price

'''
*** carts() displays the items in the current user's cart and saved list if the current user is logged in
    @param: none
    @return: rendering of product page
'''  
@bp.route('/carts', methods = ['GET', 'POST'])
def carts():
    #check if valid attempt
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    #gather values that must be displayed on page
    form3 = submitOrderForm()
    uid = current_user.id
    products = Cart.get(uid)
    x = datetime.datetime.now()
    savedProducts = Cart.getSaved(uid)
    return render_template('cart.html',
                           printprods = products,
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = form3,
                           time = x,
                           savedProducts = savedProducts)


'''
*** changeCart(uid, pid, newValue) is called when a user wants to adjust the number of a certain product in their cart.
    @param: uid = user ID, pid = product ID, newValue = value to update product quantity
    @return: carts page rendering after database change is made
'''      
@bp.route('/carts/<uid>,<pid>,<newValue>', methods = ['GET', 'POST'])
def changeCart(uid, pid, newValue):
    #check if valid chage
    if int(newValue)<1:
        newValue = str(1)
        
    #change cart database
    products = Cart.updateCount(uid, pid, newValue)
    
    #store other values that must be rendered on page
    submitForm = submitOrderForm()
    x = datetime.datetime.now()
    savedProducts = Cart.getSaved(uid)

    return render_template('cart.html',
                           printprods = products,
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm,
                           time = x,
                           savedProducts = savedProducts)

'''
*** saveItem(uid, pid, saved) allows a user to save an item from their cart to "saved for later".
    @param: uid = current user ID, pid = product ID to save, saved = saved status
    @return: rendering of carts page after database change
'''      
@bp.route('/carts/saved/<uid>,<pid>,<saved>', methods = ['GET', 'POST'])
def saveItem(uid, pid, saved):
    #save item for later and gather cart information
    savedProducts = Cart.saveForLater(uid, pid, saved)
    products = Cart.get(uid)
    
    #gather information to be rendered
    submitForm = submitOrderForm()
    x = datetime.datetime.now()
    return render_template('cart.html',
                           printprods = products, 
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm, 
                           time = x,
                           savedProducts=savedProducts)
 
'''
*** moveItem(uid, pid, saved) allows a user to move an item from "saved for later" to their cart.
    @param: uid = current user ID, pid = product ID to save, saved = saved status
    @return: rendering of carts page after database change
'''       
@bp.route('/carts/move/<uid>,<pid>,<saved>', methods = ['GET', 'POST'])
def moveItem(uid, pid, saved):
    #move item to active cart and get saved products and active products
    savedProducts = Cart.moveItem(uid, pid, saved)
    products = Cart.get(uid)
    
    #gather information to render on page
    submitForm = submitOrderForm()
    x = datetime.datetime.now()
    return render_template('cart.html',
                           printprods = products, 
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm, 
                           time = x,
                           savedProducts=savedProducts)
       
'''
*** delete_product(user_id, purchase_id) allows a user to delete an item from their cart or from "saved for later".
    @param: user_id = current user ID, purchase_id = product ID for the purchase
    @return: rendering of carts page after database change
'''       
@bp.route('/carts/<user_id>,<purchase_id>', methods=['GET','DELETE'])
def delete_product(user_id, purchase_id):
    #delete the product from the cart
    products = Cart.delete_product(user_id, purchase_id)
    
    #gather data to be rendered on page
    submitForm = submitOrderForm()
    x = datetime.datetime.now()
    savedProducts = Cart.getSaved(user_id)
    return render_template('cart.html',
                           printprods = products, 
                           numItems = getNumItems(products),
                           totalPrice = getTotalPrice(products),
                           form3 = submitForm, 
                           time = x,
                           savedProducts=savedProducts)

'''
*** submitOrder(user_id, time) allows a user to submit an order to write information to purchases. A series of checks
    are made to ensure validity of order. Buyer balance is decreased, seller balance is increased, inventory is
    decreased, and the cart is emptied.
    @param: user_id = current user ID, time = time of submission
    @return: rendering of submission page.
'''  
    
@bp.route('/submitOrder/<user_id>,<time>', methods = ['GET','POST','DELETE'])
def submitOrder(user_id, time):
    form3 = submitOrderForm()
    orderProducts = list(Cart.get(current_user.id))
    
    #check if valid order
    if len(orderProducts)<1:
        message="You cannot submit an empty cart."
        return render_template('cart.html',
                           printprods = orderProducts,
                           numItems = getNumItems(orderProducts),
                           totalPrice = getTotalPrice(orderProducts),form3=form3,
                           time = time, message=message)
    for prod in orderProducts:
        availableQuant = Inventory.get_from_pid_specific(prod.pid, prod.sid).quantity
        if prod.quantity>availableQuant:
            message = "Your seller does not have enough inventory. Please adjust your order." + str(prod.sid) + str(prod.u_price)
            return render_template('cart.html',
                           printprods = orderProducts,
                           numItems = getNumItems(orderProducts),
                           totalPrice = getTotalPrice(orderProducts),form3=form3,
                           time = time, message=message)
            
    #decrease inventory and increase user balance
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
    
