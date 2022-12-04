from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.inventory import Inventory
from .models.product import Product

from flask import Blueprint

bp = Blueprint('inventories', __name__)

class InventorySearch(FlaskForm):
    inventory_id = IntegerField('Product id: ')
    product_id = IntegerField('Product id: ')
    quantity = IntegerField('Quantity: ')
    price = FloatField('Price: ')
    submit = SubmitField('ADD')

class AddNewProductForm(FlaskForm):
    name = StringField('Name: ')
    description = StringField('Description: ')
    image = StringField('Photo: ')
    category = StringField('Category: ')
    quantity = IntegerField('Quantity: ')
    price = FloatField('Price: ')
    submit = SubmitField('ADD NEW PRODUCT')

class UpdateProductName(FlaskForm):
    name = StringField('New Name: ', validators=[DataRequired()])
    submit = SubmitField('ADD NEW PRODUCT')


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
    return redirect(url_for('inventories.inventory'))
    
 

@bp.route('/inventory/addNewProductPage', methods=['GET', 'POST'])
def addNewProductPage():
    form = AddNewProductForm()
    return render_template('add_product_page.html',
                            form = form) 

@bp.route('/inventory/addNewProduct', methods=['GET', 'POST'])
def addNewProduct():
    seller_id = current_user.id
    form = AddNewProductForm()
    name = form.name.data
    description = form.description.data
    price = form.price.data
    quantity = form.quantity.data
    image = form.image.data
    category = form.category.data
    
    Inventory.add_new_product(seller_id, name,description,price,quantity,image,category)

    return redirect(url_for('inventories.inventory'))
                           #if available not true then how to become a seller?


@bp.route('/inventory/editProduct/<pid>', methods=['GET', 'POST'])
def editProduct(pid):
    product_details = Product.get(pid)
    return render_template('edit-product.html', pid = pid, product_details = product_details)
                           #if available not true then how to become a seller?
# @bp.route('/inventory/editProduct/<sid>,<pid>', methods=['GET', 'POST'])
# def editProduct(sid,pid):
#     product_details = Product.get(pid)
#     return render_template('edit-product.html', sid = sid, pid = pid, product_details = product_details)
#                            #if available not true then how to become a seller?


# @bp.route('/inventory/editProduct/<sid>,<pid>/update-name', methods=['GET', 'POST'])
@bp.route('/inventory/editProduct/updateName/<pid>', methods=['GET', 'POST'])
def update_name(pid):
    
    form = UpdateProductName()
    # user_id = current_user.id
    new_name = form.name.data
    
    # user_id = current_user.id
    if form.validate_on_submit():
        Product.update_product_name(pid, new_name)      

    if request.method == "POST":
        return redirect(url_for('inventories.inventory'))


    return render_template('update-product-name.html', pid = pid, 
                                form=form)

    # if request.method == "POST":
    #     return redirect(url_for('users.get_account_info'))

    # return render_template('user/update-name.html', 
    #                        title='Update Name', 
    #                        form=form)





    # return render_template('update-product-name.html', sid = sid, pid = pid,
    #                             title='Update Product Name', 
    #                             form1=form1)


