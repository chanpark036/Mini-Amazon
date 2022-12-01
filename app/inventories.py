from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.inventory import Inventory

from flask import Blueprint

bp = Blueprint('inventories', __name__)

class InventorySearch(FlaskForm):
    inventory_id = IntegerField('Product id: ')
    product_id = IntegerField('Product id: ')
    quantity = IntegerField('Quantity: ')
    price = FloatField('Price: ')
    submit = SubmitField('ADD')

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = InventorySearch()
    seller_id = current_user.id
    available = True
    inv = Inventory.get(seller_id)
    return render_template('inventory.html',
                            sid = seller_id,
                           inventory_products=inv, form=form, available = available) 
                           #if available not true then how to become a seller?

@bp.route('/inventory/<uid>,<pid>,<new_q>', methods = ['GET', 'POST'])
def modifyQuantity(uid, pid, new_q):
    products = Inventory.change_q(uid, pid, new_q)
    form = InventorySearch()
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                            sid = uid,
                           inventory_products = products, form=form, available = True)
    
@bp.route('/inventory/<uid>,<pid>', methods=['GET','DELETE'])
def removeProduct(uid, pid):
    products = Inventory.remove(uid, pid)
    form = InventorySearch()
    return render_template('inventory.html',
                            sid = uid,
                           inventory_products = products, form=form, available = True)

@bp.route('/inventory/add', methods=['GET','POST'])
def addProduct(): #ensure that pid is not already in database and if is then give error
    #pid could be in database already but under a different seller
    seller_id = current_user.id
    uid = seller_id #change
    form = InventorySearch()
    pid = form.product_id.data
    quantity = form.quantity.data
    u_price = form.price.data
    products = Inventory.add(uid, pid, quantity,u_price)
    return render_template('inventory.html',
                           sid = uid,
                           inventory_products = products, form=form, available = True)
    


