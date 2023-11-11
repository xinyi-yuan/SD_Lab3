from flask import Flask, render_template, request, flash, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "0000"


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run()