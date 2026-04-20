from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "success")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1️⃣ Empty field check
        if not username or not password:
            flash("Please fill in all fields.", "error")
            return render_template('login.html', user=current_user)

        # 2️⃣ Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Username does not exist.", "error")
            return render_template('login.html', user=current_user)

        # 3️⃣ Password validation
        if not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.", "error")
            return render_template('login.html', user=current_user)

        # 4️⃣ Success
        login_user(user)
        flash("Login successful. Welcome back!", "success")
        return redirect(url_for('views.home'))

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        flash("You already have an account.", "success")
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 1️⃣ Empty fields
        if not email or not username or not password1 or not password2:
            flash("All fields are required.", "error")
            return render_template('sign_up.html', user=current_user)

        # 2️⃣ Email format check
        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "error")
            return render_template('sign_up.html', user=current_user)

        # 3️⃣ Username exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "error")
            return render_template('sign_up.html', user=current_user)

        # 4️⃣ Email exists
        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", "error")
            return render_template('sign_up.html', user=current_user)

        # 5️⃣ Password match
        if password1 != password2:
            flash("Passwords do not match.", "error")
            return render_template('sign_up.html', user=current_user)

        # 6️⃣ Password strength
        if len(password1) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template('sign_up.html', user=current_user)

        # 7️⃣ Create user
        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password1)
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account created successfully!", "success")
        return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)

