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


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if current_user.is_authenticated:
        form = FeedbackSearch()
        user_id = current_user.id
        feedback = Feedback.get_all_by_uid(user_id)

        return render_template('feedback.html',
                           user_feedback=feedback, form = form, uid = user_id)
    return redirect(url_for('users.login'))

@bp.route('/review-product/<product_id>', methods=['GET', 'POST'])
def review_product(product_id):
    form = PostFeedback()
    user = current_user.id
    if request.method == "POST":
        Feedback.add_p_review( user,
                            product_id,
                         form.review.data,
                         form.rating.data)
        return redirect(url_for('products.detail_product', product_id=product_id))
    return render_template('review-product.html', title='Review Product', form=form)

@bp.route('/review-seller/<seller_id>', methods=['GET', 'POST'])
def review_seller(seller_id):
    form = PostFeedback()
    user = current_user.id
    if request.method == "POST":
        Feedback.add_s_review( user,
                            seller_id,
                         form.review.data,
                         form.rating.data)
        return redirect(url_for('feedback.feedback'))
    return render_template('review-seller.html', title='Review Seller', form=form)

@bp.route('/update-review/<review_id>', methods=['GET', 'POST'])
def update_review(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_review(review_id,
                         form.review.data)
        return redirect(url_for('feedback.feedback'))
    review = Feedback.get(review_id)
    return render_template('update-review.html', title='Update Review', form=form, review_id=review_id, review=review)

@bp.route('/update-rating/<review_id>', methods=['GET', 'POST'])
def update_rating(review_id):
    form = UpdateFeedback()
    if request.method == "POST":
        Feedback.update_rating(review_id,
                         form.rating.data)
        return redirect(url_for('feedback.feedback'))
    rating = Feedback.get(review_id)
    return render_template('update-rating.html', title='Update Rating', form=form, review_id=review_id, rating=rating)

@bp.route('/feedback/<review_id>', methods=['GET','DELETE'])
def delete_review(review_id):
    Feedback.delete_review(review_id)
    return redirect(url_for('feedback.feedback'))

@bp.route('/review-summary/<type>/<id>', methods=['GET', 'POST'])
def summarize_reviews(type, id):
    if type == 'p':
        reviews = Feedback.get_all_by_pid(id)
        stats = Feedback.get_p_stats(id)
        rating = Feedback.get_p_ratings(id)
    else:
        reviews = Feedback.get_all_by_sid(id)
        stats = Feedback.get_s_stats(id)
        rating = Feedback.get_s_ratings(id)
    ratings = create_rating(rating)
    return render_template('review-summary.html', title='Reviews', reviews=reviews, stats=stats, ratings=ratings)