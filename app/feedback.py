import datetime
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from faker import Faker

from .models.product import Product
from .models.feedback import Feedback
from .models.user import User

from flask import Blueprint
bp = Blueprint('feedback', __name__)

Faker.seed(0)
fake = Faker()


class FeedbackSearch(FlaskForm):
    user_id = IntegerField('User id')
    search = SubmitField('Search')

class PostFeedback(FlaskForm):
    review = TextAreaField('Review')
    user_id = IntegerField('User ID')
    rating = SelectField('Rating', choices=[1,2,3,4,5])
    product_id = IntegerField('Product ID')
    seller_id = IntegerField('Seller ID')
    image = TextAreaField('Image URL (optional)')
    submit = SubmitField('Submit')

class UpdateFeedback(FlaskForm):
    review_id = IntegerField('Review ID')
    review = TextAreaField('New Text')
    rating = SelectField('Rating', choices=[1,2,3,4,5])
    image = TextAreaField('Image URL (optional)')
    submit = SubmitField('Submit')

class orderBy(FlaskForm):
    order = SelectField('Order' , choices=[('submitted_timestamp','Most Recent'), ('upvotes', 'Most Helpful'), ('rating', 'Rating')])
    submit = SubmitField('Submit')


'''
*** review_product(product_id) displays the form to submit a product review
    @param: product_id: the unique id of the product
    @return: rendering of submit review page
''' 
@bp.route('/review-product/<product_id>', methods=['GET', 'POST'])
def review_product(product_id):
    form = PostFeedback()
    user = current_user.id
    if request.method == "POST":
        if len(form.image.data) == 0:
            image = "NA"
        else:
            image = form.image.data
        Feedback.add_p_review( user,
                            product_id,
                    form.review.data,
                    form.rating.data,
                    0,
                    image)
        return redirect(url_for('products.detail_product', product_id=product_id))
    return render_template('feedback/review-product.html', title='Review Product', form=form)

'''
*** review_seller(seller_id) displays the form to submit a seller review
    @param: seller_id: the unique user id of the seller
    @return: rendering of submit review page
''' 
@bp.route('/review-seller/<seller_id>', methods=['GET', 'POST'])
def review_seller(seller_id):
    form = PostFeedback()
    user = current_user.id
    if request.method == "POST":
        if len(form.image.data) == 0:
            image = "NA"
        else:
            image = form.image.data
        Feedback.add_s_review( user,
                            seller_id,
                         form.review.data,
                         form.rating.data,
                         0,
                    image)
        return redirect(url_for('users.get_user_public_view', uid=seller_id))
    return render_template('feedback/review-seller.html', title='Review Seller', form=form)

'''
*** update_review(review_id) displays the current review text and form to submit new text
    @param: review_id: the unique id of the review
    @return: rendering of edit review page
''' 
@bp.route('/update-review/<review_id>', methods=['GET', 'POST'])
def update_review(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_review(review_id,
                         form.review.data)
        return redirect(url_for('users.get_account_info'))
    review = Feedback.get(review_id)
    return render_template('feedback/update-review.html', title='Update Review', form=form, review_id=review_id, review=review)

'''
*** update_rating(review_id) displays the current rating and form to submit a new rating
    @param: review_id: the unique id of the review
    @return: rendering of edit review page
''' 
@bp.route('/update-rating/<review_id>', methods=['GET', 'POST'])
def update_rating(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_rating(review_id,
                         form.rating.data)
        return redirect(url_for('users.get_account_info'))
    rating = Feedback.get(review_id)
    return render_template('feedback/update-rating.html', title='Update Rating', form=form, review_id=review_id, rating=rating)

'''
*** update_image(review_id) displays the current image and form to submit a new image url
    @param: review_id: the unique id of the review
    @return: rendering of edit review page
''' 
@bp.route('/update-image/<review_id>', methods=['GET', 'POST'])
def update_image(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_image(review_id,
                         form.image.data)
        return redirect(url_for('users.get_account_info'))
    image = Feedback.get(review_id)
    return render_template('feedback/update-image.html', title='Update Image', form=form, review_id=review_id, image=image)

'''
*** delete_review(review_id) deletes a review and re-renders the account page
    @param: review_id: the unique id of the review
    @return: rendering of account page
''' 
@bp.route('/feedback/<review_id>', methods=['GET','DELETE'])
def delete_review(review_id):
    Feedback.delete_review(review_id)
    return redirect(url_for('users.get_account_info'))

'''
*** update_votes(review_id, upvotes, product_id) updates the upvotes of a review on the product page and re-renders the page
    @param: review_id, upvotes, product_id: the unique id of the review, number of upvotes, the unique id of the product
    @return: rendering of product detail page
''' 
@bp.route('/product-detail/<product_id>/<review_id>/<upvotes>', methods=['GET', 'POST'])
def update_votes(review_id, upvotes, product_id):
    Feedback.update_votes(review_id, upvotes)
    return redirect(url_for('products.detail_product', product_id=product_id))

'''
*** update_s_votes(seller_id, review_id, upvotes) updates the upvotes of a review on the seller page and re-renders the page
    @param: seller_id, review_id, upvotes: the unique user id of the seller, the unique id of the review, number of upvotes
    @return: rendering of seller detail page
''' 
@bp.route('/userpublicview/<seller_id>/<review_id>/<upvotes>', methods=['GET', 'POST'])
def update_s_votes(review_id, upvotes, seller_id):
    Feedback.update_votes(review_id, upvotes)
    return redirect(url_for('users.get_user_public_view', uid = seller_id))
