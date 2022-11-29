from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchases', __name__)

class SearchUserPurchases(FlaskForm):
    user_id = IntegerField('User id')
    search = SubmitField('Search')

@bp.route('/searchuserpurchases', methods=['GET', 'POST'])
def user_purchases():
    form = SearchUserPurchases()
    uid = form.user_id.data
    purchases = Purchase.get_all_user_purchases(uid)
    return render_template('user_purchases.html', 
                            purchase_history=purchases,
                            form=form)
    
@bp.route('/purchasehistory')
def purchase_history():
    purchases = Purchase.get_order_history_information(current_user.id)
    return render_template('purchase_history.html',
                            purchase_history=purchases)
    
def getTotalPrice(productList):
    price = 0
    for prod in productList:
        price+=prod.total_price
    return price

@bp.route('/detailedOrderPage/<user_id>,<time_purchased>', methods = ['GET','POST','DELETE'])
def detailed_order_page(user_id, time_purchased):
    orderDetails = Purchase.get_detailed_order_page(current_user.id, time_purchased)
    total_cost = getTotalPrice(orderDetails)
    
    return render_template('detailed-order-page.html',
                           orderDetails=orderDetails,
                           time_purchased=time_purchased,
                           total=total_cost)