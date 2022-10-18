import datetime
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product
from .models.feedback import Feedback

from flask import Blueprint
bp = Blueprint('feedback', __name__)


class FeedbackSearch(FlaskForm):
    user_id = IntegerField('User id')
    search = SubmitField('Search')


@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackSearch()
    user_id = form.user_id.data
    feedback = Feedback.get_recent_k(user_id, 5)

    return render_template('feedback.html',
                           user_feedback=feedback, form = form, uid = user_id)