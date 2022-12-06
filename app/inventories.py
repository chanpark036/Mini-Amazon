from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, SelectField
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

available_categories = ['Apps', 'Food', 'Books', 'Electronics', 'Health', 'Outdoor', 'Entertainment']

class AddNewProductForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    description = StringField('Description: ')
    image = StringField('Photo: ')    
    category = SelectField('Category: ', choices = available_categories, validators=[DataRequired()])
    quantity = IntegerField('Quantity: ')
    price = FloatField('Price: ')
    submit = SubmitField('ADD NEW PRODUCT')

class UpdateProductName(FlaskForm):
    name = StringField('New Name: ', validators=[DataRequired()])
    submit = SubmitField('UPDATE NAME')

class UpdateProductCategory(FlaskForm):
    # available_categories = ['Apps', 'Food', 'Books', 'Electronics', 'Health', 'Outdoor', 'Entertainment']
    name = SelectField('New Category: ', choices = available_categories, validators=[DataRequired()])
    submit = SubmitField('UPDATE CATEGORY')

class UpdateProductDescription(FlaskForm):
    name = StringField('New Description: ', validators=[DataRequired()])
    submit = SubmitField('UPDATE DESCRIPTION')

class UpdateProductImage(FlaskForm):
    name = StringField('New Image URL: ', validators=[DataRequired()])
    submit = SubmitField('UPDATE IMAGE')



@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = InventorySearch()
    seller_id = current_user.id
    if Inventory.verify_seller(seller_id):
        available = True
        inv = Inventory.get(seller_id)
        for p in inv:
            p.name = Inventory.get_name_from_pid(p.pid)
    else:
        available = False
        inv = []
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
    return redirect(url_for('inventories.inventory'))
    # return render_template('inventory.html',
    #                         sid = uid,
    #                        inventory_products = products, form=form, available = True)
    
@bp.route('/inventory/<uid>,<pid>', methods=['GET','DELETE'])
def removeProduct(uid, pid):
    products = Inventory.remove(uid, pid)
    form = InventorySearch()
    return redirect(url_for('inventories.inventory'))
    # return render_template('inventory.html',
    #                         sid = uid,
    #                        inventory_products = products, form=form, available = True)

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

@bp.route('/inventory/editProduct/updateDescription/<pid>', methods=['GET', 'POST'])
def update_description(pid):
    
    form = UpdateProductDescription()
    # user_id = current_user.id
    new_desc = form.name.data
    
    # user_id = current_user.id
    if form.validate_on_submit():
        Product.update_product_description(pid, new_desc)      

    if request.method == "POST":
        return redirect(url_for('inventories.inventory'))


    return render_template('update-product-name.html', pid = pid, 
                                form=form)

@bp.route('/inventory/editProduct/updateCategory/<pid>', methods=['GET', 'POST'])
def update_category(pid):
    
    form = UpdateProductCategory()
    # user_id = current_user.id
    new_cat = form.name.data
    
    # user_id = current_user.id
    if form.validate_on_submit():
        Product.update_product_category(pid, new_cat)      

    if request.method == "POST":
        return redirect(url_for('inventories.inventory'))


    return render_template('update-product-name.html', pid = pid, 
                                form=form)

@bp.route('/inventory/editProduct/updateImage/<pid>', methods=['GET', 'POST'])
def update_image(pid):
    
    form = UpdateProductImage()
    # user_id = current_user.id
    new_imgurl = form.name.data
    
    # user_id = current_user.id
    if form.validate_on_submit():
        Product.update_product_image(pid, new_imgurl)      

    if request.method == "POST":
        return redirect(url_for('inventories.inventory'))


    return render_template('update-product-name.html', pid = pid, 
                                form=form)

@bp.route('/inventory/line',methods=['GET'])
def charts():
    seller_id = current_user.id

    #line_graph
    line_labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]
    times = Inventory.times_bought_from_seller(seller_id)
    line_values = [0 for i in range(12)]
    for time in times:
        line_values[time[0].month-1]+=1

    #pie_graphs
    users = Inventory.users_buying_from_seller(seller_id)
    user_freqs = {}
    colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    for firstname,lastname in users:
        user = firstname + " " + lastname
        user_freqs[user] = user_freqs.get(user,0)+1
    if user_freqs:
        keys, values = zip(*user_freqs.items())
    else:
        keys=[]
        values=[]

    #bar_graphs
    p_names = Inventory.product_popularity(seller_id)
    p_freqs={}
    for name in p_names:
        p_freqs[name[0]] = p_freqs.get(name[0],0)+1
    if p_freqs:
        p_keys, p_values = zip(*p_freqs.items())
    else:
        p_keys=[]
        p_values=[]

    
    line_max = 10 if not line_values else max(line_values)
    bar_max = 10 if not p_values else max(p_values)

    return render_template('inventory_charts.html', 
                    line_max=line_max, line_labels=line_labels, line_values=line_values,
                    chart_max = min(12,len(keys)), chart_set=zip(values[:min(12,len(keys))], keys[:min(12,len(keys))], colors[:min(12,len(keys))]),
                    bar_max = bar_max, bar_labels = p_keys, bar_values = p_values)
