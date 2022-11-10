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

class ProductsKInput(FlaskForm):
    value = IntegerField('Get top k expensive products') or 0
    search = SubmitField('Search')

@bp.route('/products', methods = ['GET', 'POST'])
def index():    


    form = ProductsKInput()

    
    k = form.value.data
    
    if k is None:
        products = []
    else:
        products = Product.get_top_K_expensive(True, k)

    return render_template('products.html',
                           avail_products=products, form = form)

#   

# class FilterProductCategory(FlaskForm):
#     category = SubmitField('Enter Category')

# @bp.route('/products', methods = ['GET', 'POST'])
# def index():    


#     form = FilterProductCategory()
#     category = form.category.data
    
#     products = filterByCategory(category)
    

#     return render_template('products.html',
#                            avail_products=products, form = form)

