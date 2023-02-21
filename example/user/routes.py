from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user

from example import bcrypt, db
from example.user.forms import LoginForm, RegisterForm
from example.user.models import User

user_bp = Blueprint(
    'user',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.home'))
    return render_template('user/login.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))
