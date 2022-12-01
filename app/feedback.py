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
    submit = SubmitField('Submit')

class UpdateFeedback(FlaskForm):
    review_id = IntegerField('Review ID')
    review = TextAreaField('New Text')
    rating = SelectField('Rating', choices=[1,2,3,4,5])
    submit = SubmitField('Submit')

class orderBy(FlaskForm):
    order = SelectField('Order' , choices=[('submitted_timestamp','Most Recent'), ('upvotes', 'Most Helpful'), ('rating', 'Rating')])
    submit = SubmitField('Submit')


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if current_user.is_authenticated:
        form = FeedbackSearch()
        form1 = orderBy()
        user_id = current_user.id
        product_feedback = Feedback.get_all_by_uid_pid_help(user_id)
        seller_feedback = Feedback.get_all_by_uid_sid_help(user_id)
        return render_template('feedback/feedback.html', 
                           product_feedback=product_feedback, seller_feedback=seller_feedback, form = form, uid = user_id, form1 = form1)
    return redirect(url_for('users.login'))

@bp.route('/review-product/<product_id>', methods=['GET', 'POST'])
def review_product(product_id):
    form = PostFeedback()
    user = current_user.id
    if request.method == "POST":
        Feedback.add_p_review( user,
                            product_id,
                    form.review.data,
                    form.rating.data,
                    0)
        return redirect(url_for('products.detail_product', product_id=product_id))
    return render_template('feedback/review-product.html', title='Review Product', form=form)

@bp.route('/review-seller/<seller_id>', methods=['GET', 'POST'])
def review_seller(seller_id):
    form = PostFeedback()
    user = current_user.id
    if request.method == "POST":
        Feedback.add_s_review( user,
                            seller_id,
                         form.review.data,
                         form.rating.data,
                         0)
        return redirect(url_for('feedback.feedback'))
    return render_template('feedback/review-seller.html', title='Review Seller', form=form)

@bp.route('/update-review/<review_id>', methods=['GET', 'POST'])
def update_review(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_review(review_id,
                         form.review.data)
        return redirect(url_for('feedback.feedback'))
    review = Feedback.get(review_id)
    return render_template('feedback/update-review.html', title='Update Review', form=form, review_id=review_id, review=review)

@bp.route('/update-rating/<review_id>', methods=['GET', 'POST'])
def update_rating(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_rating(review_id,
                         form.rating.data)
        return redirect(url_for('feedback.feedback'))
    rating = Feedback.get(review_id)
    return render_template('feedback/update-rating.html', title='Update Rating', form=form, review_id=review_id, rating=rating)

@bp.route('/feedback/<review_id>', methods=['GET','DELETE'])
def delete_review(review_id):
    Feedback.delete_review(review_id)
    return redirect(url_for('feedback.feedback'))

@bp.route('/product-detail/<product_id>/<review_id>/<upvotes>', methods=['GET', 'POST'])
def update_votes(review_id, upvotes, product_id):
    Feedback.update_votes(review_id, upvotes)
    return redirect(url_for('products.detail_product', product_id=product_id))

@bp.route('/userpublicview/<seller_id>/<review_id>/<upvotes>', methods=['GET', 'POST'])
def update_s_votes(review_id, upvotes, seller_id):
    Feedback.update_votes(review_id, upvotes)
    return redirect(url_for('users.get_user_public_view'))
