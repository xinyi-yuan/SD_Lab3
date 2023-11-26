import os
import psycopg2
from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "0000"

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL set for Flask application")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/xinyi")
def xinyi():
    return render_template("xinyi.html")


@app.route("/hannah")
def hannah():
    return render_template("hannah.html")


@app.route("/will")
def will():
    return render_template("will.html")


@app.route("/nathan")
def nathan():
    return render_template("nathan.html")


@app.route("/project")
def project():
    return render_template("project.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pword']

        cur = conn.cursor()
        cur.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        # Check if user exists and the password is correct
        if user and check_password_hash(user[1], password):
            flash("Login Successful!")
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password, try again')
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pword']
        confirm_pword = request.form['pword2']
        user_name = request.form['name']

        if password != confirm_pword:
            flash('Passwords do no match!')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (email, password, user_name) VALUES (%s, %s, %s)",
            (email, hashed_password, user_name))
            conn.commit()
            cur.close()
            flash("Account created successfully!")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash("Error: " + str(e))
            return redirect(url_for('sign_up'))
    return render_template("signup.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/reset")
def reset():
    return render_template("reset.html")


if __name__ == "__main__":
    app.run(debug=True)
