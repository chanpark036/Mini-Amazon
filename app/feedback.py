import datetime
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from faker import Faker

from .models.product import Product
from .models.feedback import Feedback

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
    rating = IntegerField('Rating')
    product_id = IntegerField('Product ID')
    seller_id = IntegerField('Seller ID')
    submit = SubmitField('Submit')


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackSearch()
    user_id = form.user_id.data
    feedback = Feedback.get_recent_k(user_id, 5)

    return render_template('feedback.html',
                           user_feedback=feedback, form = form, uid = user_id)

@bp.route('/review', methods=['GET', 'POST'])
def review():
    form = PostFeedback()
    time = datetime.datetime.now()
    user = 3
    if Feedback.add_review( user,
                         form.review.data,
                         form.rating.data):
        flash('Thanks for writing a review!')
    return render_template('review.html', title='Review', form=form)