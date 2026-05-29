from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('home.html', title='Home')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('patient.dashboard'))
    if request.method == 'POST':
        full_name        = request.form.get('full_name')
        email            = request.form.get('email')
        phone            = request.form.get('phone')
        password         = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(full_name=full_name, email=email, phone=phone,
                    password=hashed_pw, role='patient')
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('patient.dashboard'))
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('patient.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', title='Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.home'))
