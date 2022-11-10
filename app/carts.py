from flask import render_template
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
@bp.route('/carts', methods = ['GET', 'POST'])
def carts():
    # get all available products for sale:
    #uid=keyboard input field
    form1 = enterID()
    form2 = updateData()
    uid = form1.uid.data
    products = Cart.get(uid)
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           form1 = form1, form2 = form2)
@bp.route('/changeCart', methods = ['GET', 'POST'])
def changeCart():
    searchForm = enterID()
    updateForm = updateData()
    newValue = updateForm.quantity.data
    pid = updateForm.pid.data
    products = Cart.updateCount(pid, newValue)
    print(products)
    # find the products current user has bought:
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           printprods = products,
                           form1 = searchForm,
                           form2 = updateForm)
