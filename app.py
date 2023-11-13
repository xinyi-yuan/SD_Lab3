from flask import Flask, render_template, request, flash, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "0000"


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


@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run()
