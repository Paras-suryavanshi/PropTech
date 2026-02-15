from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from app.extensions import db
from app.models import User

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Grab all the fields from the form
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        role = request.form.get('role') # 'tenant' or 'technician'

        # Check if username OR email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.')
            return redirect(url_for('auth.register'))

        # Hash password
        hashed_password = generate_password_hash(password)
        
        # tenants get auto-approved, techs need manager review
        auto_approve = True if role == 'tenant' else False
        
        # set initial approval flag based on role
        new_user = User(
            username=username, 
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password_hash=hashed_password, 
            role=role,
            is_approved=auto_approve
        )
        
        db.session.add(new_user)
        db.session.commit()

        # --- DYNAMIC FLASH MESSAGE ---
        if role == 'tenant':
            flash('Registration successful! You can now log in and report issues.')
        else:
            flash('Registration successful! Please log in to await Manager approval.')
            
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash("Login failed. Check your username and password.")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password')
def forgot_password():
    # temp redirect to manager to save time
    flash('For security reasons, please contact your Property Manager (manager@qwego.com) to reset your password.', 'info')
    return redirect(url_for('auth.login'))