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
cur = conn.cursor()

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


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/reset")
def reset():
    return render_template("reset.html")


if __name__ == "__main__":
    app.run(debug=True)
