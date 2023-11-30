# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return 'Home Page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simulate a high-severity vulnerability: SQL Injection
        # This is a security vulnerability; DO NOT use this in production code
        query = f"SELECT * FROM User WHERE username = '{username}' AND password = '{password}'"
        user = db.session.execute(query).fetchone()

        # Simulate a medium-severity vulnerability: Use of insecure MD5 hash for password storage
        # This is a security vulnerability; DO NOT use this in production code
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        user = User.query.filter_by(username=username, password=hashed_password).first()

        if user and hashed_password == user.password:
            login_user(User(id=user.id, username=user.username))
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your username and password.', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
