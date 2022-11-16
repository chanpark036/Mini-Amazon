from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('products', __name__)

from .models.product import Product
from .models.purchase import Purchase


###
class ProductsKInput(FlaskForm):
    value = IntegerField('Get top k expensive products') or 0
    search = SubmitField('Search')

# @bp.route('/products', methods = ['GET', 'POST'])
# def index():    

#     # form corresponds with top K
#     form = ProductsKInput()

#     k = form.value.data
    
#     if k is None:
#         products = []
#     else:
#         products = Product.filterByCategory(k)

#     return render_template('products.html',
#                            avail_products=products, form = form)

class ProductsKInput(FlaskForm):
    value = IntegerField('Get top k expensive products') or 0
    search = SubmitField('Search')

class FilterProductCategory(FlaskForm):
    category = StringField('Enter Name')
    search = SubmitField('Enter Name')


@bp.route('/products', methods = ['GET', 'POST'])
def index():    

    # form corresponds with top K
    form1 = ProductsKInput()
    form2 = FilterProductCategory()
    # k = form1.value.data
    
    # if k is None:
    #     products = []
    # else:
    #     products = Product.get_top_K_expensive(True, k)

    products = Product.get_all(True)    
    return render_template('products.html',
                           avail_products=products, form1 = form1, form2 = form2)

#   


@bp.route('/productCategory', methods = ['GET', 'POST'])
def productCategory():    
    
    form1 = ProductsKInput()
    form2 = FilterProductCategory()
    category = form2.category.data
    
    products = Product.filterByCategory(category)
    
    return render_template('products.html',
                           products_by_category=products, form1 = form1, form2 = form2)

