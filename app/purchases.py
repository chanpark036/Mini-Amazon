from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchases', __name__)

# class SearchUserPurchases(FlaskForm):
#     user_id = IntegerField('User id')
#     search = SubmitField('Search')

# @bp.route('/searchuserpurchases', methods=['GET', 'POST'])
# def user_purchases():
#     form = SearchUserPurchases()
#     uid = form.user_id.data
#     purchases = Purchase.get_all_user_purchases(uid)
#     return render_template('user/user_purchases.html', 
#                             purchase_history=purchases,
#                             form=form)
    
@bp.route('/purchasehistory', methods=['GET', 'POST'])
def purchase_history():
    if current_user.is_authenticated:
        purchase_history = Purchase.get_purchase_history(current_user.id)
        return render_template('user/purchase_history.html',
                                purchase_history=purchase_history)
    return redirect(url_for('users.login'))
    
# get total cost of a list of products
def get_total_price(productList):
    price = 0
    for prod in productList:
        price += prod.total_price
    return price

@bp.route('/detailedOrderPage/<user_id>/<time_purchased>', methods = ['GET','POST','DELETE'])
def detailed_order_page(user_id, time_purchased):
    if current_user.is_authenticated:
        orderDetails = Purchase.get_detailed_order_page(current_user.id, time_purchased)
        total_cost = get_total_price(orderDetails)
        return render_template('user/detailed-order-page.html',
                            orderDetails=orderDetails,
                            time_purchased=time_purchased,
                            total=total_cost)
    return redirect(url_for('users.login'))


@bp.route('/purchase_history_seller')
def purchase_history_seller():
    seller_id = current_user.id
    purchases = Purchase.get_all_seller_purchases(seller_id)
    for purchase in purchases:
        purchase.address = Purchase.get_address(purchase.uid)
    return render_template('purchase_history_seller.html', purchase_history = purchases, seller_id = seller_id)

@bp.route('/purchase_history_seller/<sid>,<uid>,<pid>,<fulfillment_status>')
def change_fulfillment(sid,uid,pid,fulfillment_status):
    purchases = Purchase.change_fulfillment(sid,uid,pid,fulfillment_status)
    return redirect(url_for('purchases.purchase_history_seller'))

