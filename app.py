from flask import Flask, render_template, request, redirect, flash, session
import dbhelper
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "deluna"

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = dbhelper.get_username(username)  

        if user and check_password_hash(user[0]["password"], password):
            session["user"] = username
            flash("Login successful!", "success")  
            return redirect("/dashboard")
        flash("Invalid username or password.", "danger") 
        return redirect("/login")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        idno = request.form["idno"]
        lastname = request.form["lastname"]
        firstname = request.form["firstname"]
        middlename = request.form["middlename"]
        course = request.form["course"]
        year_level = request.form["year_level"]
        email_address = request.form["email_address"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        success = dbhelper.register_user(lastname, firstname, middlename, course, year_level, email_address, username, password)  

        if success:
            flash("Registration successful! Please login.", "success")
            return redirect("/login")
        else:
            flash("Username already exists. Please try again with a different username.", "danger")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)