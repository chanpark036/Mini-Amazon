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
from .models.cart import Cart
from .models.feedback import Feedback
from .models.inventory import Inventory


class ProductsKInput(FlaskForm):
    value = IntegerField('Get top k expensive products') or 0
    search = SubmitField('Search')

class ProductsKInput(FlaskForm):
    value = IntegerField('Get top k expensive products') or 0
    search = SubmitField('Search')

class FilterProductCategory(FlaskForm):
    category = StringField('Enter Name')
    search = SubmitField('Enter Name')

# Reviews

def create_rating(lst):
    one,two,three,four,five = 0, 0, 0, 0, 0
    for row in lst:
        if row[0] == 1:
            one = row[1]
        if row[0] == 2:
            two = row[1]
        if row[0] == 3:
            three = row[1]
        if row[0] == 4:
            four = row[1]
        if row[0] == 5:
            five = row[1]
    return Ratings(one,two,three,four,five)


class Ratings:
    def __init__(self, one, two, three, four, five):
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.five = five

class Stats:
    def __init__(self, avg, count):
        self.avg = avg
        self.count = count

def create_stats(lst):
    if len(lst) == 0:
        return Stats("N/A", 0)
    else:
        avg = round(lst[0][1],1)
        return Stats(avg,lst[0][2])

'''
*** index() displays all available products regardless of price
    @return: products page displaying all products
'''
@bp.route('/products', methods = ['GET', 'POST'])
def index():    

    form1 = ProductsKInput()
    form2 = FilterProductCategory()

    products = Product.get_valid_products(True)    
    return render_template('products.html',
                           avail_products=products, form1 = form1, form2 = form2)


'''
*** detail_product(product_id) displays the detail view of the product with product_id
    @param: product_id = product ID
    @return: detail view of products page
'''
@bp.route('/product-detail/<product_id>', methods=['GET', 'POST'])
def detail_product(product_id):
    form1 = ProductsKInput()
    form2 = FilterProductCategory()

    #Product Details
    product_details = Product.get(product_id)

    sellers_of_product = Inventory.get_from_pid(product_id)
    
    # Reviews
    loggedIn = current_user.is_authenticated
    if loggedIn:
        user = current_user.id
        hasReview = len(Feedback.get_p_u_ratings(product_id, user)) > 0
    else:
        user = 0
        hasReview = False
    reviews = Feedback.get_all_by_pid(product_id)
    stat = Feedback.get_p_stats(product_id)
    stats = create_stats(stat)
    rating = Feedback.get_p_ratings(product_id)
    ratings = create_rating(rating)
    return render_template('product-detail.html',
                             form1 = form1, form2 = form2, product_id=product_id, reviews=reviews, stats=stats, ratings=ratings, 
                             product_details = product_details, sellers_of_product = sellers_of_product, hasReview = hasReview, loggedIn=loggedIn)

'''
*** addToCart(sid, pid, price) adds product to cart for the current user with pid, price, for a given seller 
    @param: sid = seller ID of selected product, pid = product ID, price = price of selected product
    @return: products page render
'''
@bp.route('/products/<sid>,<pid>,<price>', methods = ['GET','POST'])
def addToCart(sid,pid, price):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form1 = ProductsKInput()
    form2 = FilterProductCategory()
    products = Product.get_all(True)
    uid = current_user.id
    Cart.addProduct(uid, pid, price, sid)
    return render_template('products.html',
                           avail_products=products, form1 = form1, form2 = form2,)


'''
*** displayProductsUnder50() displays all available products with price under $50
    @return: products page under 50 render
'''
@bp.route('/products/under50', methods = ['GET','POST'])
def displayProductsUnder50():
    
    products = Product.get_valid_products_under50(True)
    
    return render_template('products_price_filter.html',
                           avail_products=products)


'''
*** displayProductsBetween50and100() displays all available products with price between (and including) $50 and $100
    @return: products page between 50 and 100 render
'''
@bp.route('/products/between50and100', methods = ['GET','POST'])
def displayProductsBetween50and100():
    
    products = Product.get_valid_products_from50to100(True)
    
    return render_template('product_price_50and100.html',
                           avail_products=products)

'''
*** displayProductsOver100() displays all available products with price over $100
    @return: products page over 100
'''
@bp.route('/products/over100', methods = ['GET','POST'])
def displayProductsOver100():
    
    products = Product.get_valid_products_over100(True)
    
    return render_template('product_price_over100.html',
                           avail_products=products)

