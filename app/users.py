from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.feedback import Feedback

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('user/login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    isseller = BooleanField('Are you a seller?', default = False)
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.isseller.data,
                         0.0,
                         form.address.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('user/register.html', 
                           title='Register', 
                           form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/account')
def get_account_info():
    if current_user.is_authenticated:
        uid = current_user.id
        product_feedback = Feedback.get_all_by_uid_pid_recent(uid)
        seller_feedback = Feedback.get_all_by_uid_sid_recent(uid)
        p_rev = len(product_feedback) > 0
        s_rev = len(seller_feedback) > 0
        user_id = User.get(current_user.id)
        return render_template('user/user_info.html', 
                               user_id=user_id, product_feedback=product_feedback, seller_feedback=seller_feedback, uid = uid, p_reviews=p_rev, s_reviews=s_rev)
    return redirect(url_for('users.login'))
 
@bp.route('/userpublicview/<uid>', methods=['GET', 'POST'])
def get_user_public_view(uid):
    user = User.get(uid)
    sid = uid
    cur_user = current_user.id
    hasReview = len(Feedback.get_s_u_ratings(sid, cur_user)) > 0
    hasPurchased = len(Feedback.check_s_u(sid,cur_user)) > 0
    reviews = Feedback.get_all_by_sid(sid)
    stat = Feedback.get_s_stats(sid)
    stats = create_stats(stat)
    rating = Feedback.get_s_ratings(sid)
    ratings = create_rating(rating)
    return render_template('user/public_view.html',
                           user=user,
                           reviews=reviews, stats=stats, ratings=ratings, seller_id = sid, hasReview=hasReview, hasPurchased=hasPurchased)


class UpdateEmail(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@bp.route('/update-email', methods=['GET', 'POST'])
def update_email():
    form = UpdateEmail()
    user_id = current_user.id
    email = form.email.data
    if form.validate_on_submit():
        if User.email_exists(email):
            return render_template('user/update-email-error.html')
        else:
            User.update_email(user_id,
                                form.email.data)
            if request.method == "POST":
                return redirect(url_for('users.get_account_info'))
            return render_template('user/update-email.html', 
                                title='Update Email', 
                                form=form)
    return render_template('user/update-email.html', 
                                title='Update Email', 
                                form=form)


class UpdatePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Submit')

# TODO: if passwords do not match, does not tell user that password change failed
@bp.route('/update-password', methods=['GET', 'POST'])
def update_password():
    form = UpdatePassword()
    user_id = current_user.id
    if form.validate_on_submit():
        User.update_password(user_id,
                             form.password.data)
    if request.method == "POST":
        return redirect(url_for('users.get_account_info'))
    return render_template('user/update-password.html', 
                           title='Update Password', 
                           form=form)


class UpdateName(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@bp.route('/update-name', methods=['GET', 'POST'])
def update_name():
    form = UpdateName()
    user_id = current_user.id
    if form.validate_on_submit():
        User.update_firstname(user_id,
                         form.firstname.data)
        User.update_lastname(user_id,
                         form.lastname.data)
    if request.method == "POST":
        return redirect(url_for('users.get_account_info'))
    return render_template('user/update-name.html', 
                           title='Update Name', 
                           form=form)


class UpdateAddress(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

@bp.route('/update-address', methods=['GET', 'POST'])
def update_address():
    form = UpdateAddress()
    user_id = current_user.id
    if form.validate_on_submit():
        User.update_address(user_id,
                         form.address.data)
    if request.method == "POST":
        return redirect(url_for('users.get_account_info'))
    return render_template('user/update-address.html', 
                           title='Update Address', 
                           form=form)


class UpdateBalance(FlaskForm):
    balance = IntegerField('Balance')
    submit = SubmitField('Submit')

# TODO: display message saying transaction not possible if new balance < 0
@bp.route('/update-balance', methods=['GET', 'POST'])
def update_balance():
    form = UpdateBalance()
    user_id = current_user.id
    curr_balance = current_user.balance
    if form.validate_on_submit():
        transaction = form.balance.data
        new_balance = curr_balance + float(transaction)
        if new_balance >= 0:
            User.update_balance(user_id, new_balance)
        else: 
            return render_template('user/update-balance-error.html')
    if request.method == "POST":
        return redirect(url_for('users.get_account_info'))
    return render_template('user/update-balance.html', 
                           title='Update Balance', 
                           form=form)