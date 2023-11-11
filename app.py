from flask import Flask, render_template, request, flash, session, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
