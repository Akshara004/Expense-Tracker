from flask import Blueprint, render_template
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from .forms import RegisterForm, LoginForm
from .models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import ExpenseForm
from app.models import Expense
import json


main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html", now=datetime.now())


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_val = form.username_or_email.data.strip()

        # Try finding user by username first
        user = User.query.filter_by(username=input_val).first()

        # If not found by username, try email
        if not user:
            user = User.query.filter_by(email=input_val).first()
        # If user exists and password matches
        if user and check_password_hash(user.password, form.password.data):
            print(f"User authenticated: {user is not None}")
            print(f"Password correct: {check_password_hash(user.password, form.password.data)}")

            login_user(user)

            from flask_login import current_user
            print(f"Is authenticated: {current_user.is_authenticated}")

            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid email or password", "danger")
    else:
        if request.method == 'POST':
            flash("Form validation failed. Check your inputs or CSRF token.", "warning")
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ExpenseForm()

    if form.validate_on_submit():
        new_expense = Expense(
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added!", "success")
        return redirect(url_for('main.dashboard'))

    # Get all expenses by the current user, sorted latest first
    all_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

    # Get current month
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Filter this month's expenses
    monthly_expenses = [e for e in all_expenses if e.date.month == current_month and e.date.year == current_year]

    # Total spent this month
    total_spent = sum(e.amount for e in monthly_expenses)

    # Breakdown by category
    category_totals = {}
    for e in monthly_expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    return render_template("dashboard.html", 
        form=form,
        expenses=monthly_expenses, 
        total=total_spent, 
        category_totals=category_totals
    )



# just for testing purposes to see the tables stored in the database
# @main.route('/show_users')
# def show_users():
#     users = User.query.all()
#     return "<br>".join([f"{u.id}: {u.username}, {u.email}, {u.password}" for u in users])

@main.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added!', category='success')
        return redirect(url_for('main.view_expenses'))
    return render_template('add_expense.html', form=form)

@main.route('/summary')
@login_required
def summary():
    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)

    # Get user's expenses for this month
    expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.date >= month_start
    ).all()

    total = sum(e.amount for e in expenses)

    # Build category-wise totals
    category_totals = {}
    for e in expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    print("labels:", labels)
    print("values:", values)

    return render_template(
        'summary.html',
        total=total,
        now=now,
        labels=labels,
        values=values
    )

# Edit Expense
@main.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        abort(403)

    form = ExpenseForm(obj=expense)

    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.description = form.description.data
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template('edit_expense.html', form=form)


# Delete Expense
@main.route('/delete_expense/<int:expense_id>', methods=['GET'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        abort(403)
    
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully.", "info")
    return redirect(url_for('main.dashboard'))


@main.route('/expenses')
@login_required
def view_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    return render_template('view_expenses.html', expenses=expenses)
