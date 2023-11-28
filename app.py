import os
import re
import psycopg2
from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "0000"
app.permanent_session_lifetime = timedelta(minutes=10)

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.environ['DATABASE_URL']
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL set for Flask application")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/xinyi")
def xinyi():
    if not is_logged_in():
        flash("Please log in to access this page.")
        return redirect(url_for('login'))
    return render_template("xinyi.html")


@app.route("/hannah")
def hannah():
    if not is_logged_in():
        flash("Please log in to access this page.")
        return redirect(url_for('login'))
    return render_template("hannah.html")


@app.route("/will")
def will():
    if not is_logged_in():
        flash("Please log in to access this page.")
        return redirect(url_for('login'))
    return render_template("will.html")


@app.route("/nathan")
def nathan():
    if not is_logged_in():
        flash("Please log in to access this page.")
        return redirect(url_for('login'))
    return render_template("nathan.html")


@app.route("/project")
def project():
    if not is_logged_in():
        flash("Please log in to access this page.")
        return redirect(url_for('login'))
    return render_template("project.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['pword']
        cur = conn.cursor()
        cur.execute("SELECT id, email, password, user_name FROM users WHERE user_name = %s", (name,))
        user = cur.fetchone()
        cur.close()

        # Check if user exists and the password is correct
        if user and check_password_hash(user[2], password):
            session['id'] = user[0]  # Storing user id in session
            session['user_name'] = user[3]
            flash(f"Welcome, {user[3]}!")
            return redirect(url_for('home'))
        else:
            flash('Invalid user name or password, try again', "error")
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pword']
        confirm_pword = request.form['pword2']
        user_name = request.form['name']

        # Check if email is in valid form
        if not check_email(email):
            flash('Email is not valid!', "error")
            return redirect(url_for('signup'))

        # Check if two password field match
        if password != confirm_pword:
            flash('Passwords do no match!', "error")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            cur = conn.cursor()

            # Check if username already exists
            cur.execute("SELECT user_name FROM users WHERE user_name = %s", (user_name,))
            exist_username = cur.fetchone()
            if exist_username:
                flash("User Name already exists. Please choose another one.", "error")
                return redirect(url_for('signup'))

            # Check if email already exists
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            exist_email = cur.fetchone()
            if exist_email:
                flash("Email already exists. Please choose another one.", "error")
                return redirect(url_for('signup'))

            # Try to insert
            cur.execute("INSERT INTO users (email, password, user_name) VALUES (%s, %s, %s)",
                        (email, hashed_password, user_name))
            conn.commit()
            cur.close()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash("Unexpected error, try again.", "error")
            return redirect(url_for('signup'))
    return render_template("signup.html")


@app.route("/forgot")
def forgot():
    return render_template("forgot.html")


@app.route("/reset")
def reset():
    return render_template("reset.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You are logged out")
    return redirect(url_for('home'))


@app.before_request
def before_request():
    session.permanent = True


# Helper function to check if current user is logged in
def is_logged_in():
    return 'id' in session


# Helper function to check if email is in valid format
def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(regex, email) is not None

if __name__ == "__main__":
    app.run(debug=True)
