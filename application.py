#Created By Danilo E Uzelin
#CS50 2021 final project
#Application for personal bar inventory control and ideas for cocktails - hope you enjoy

import os
import string
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, checkchars

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///cocktail-me.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show and control inventory"""
    drinks = db.execute("SELECT drink FROM drinks")
    inventory = db.execute(
                           "SELECT drink from inventory WHERE user_id = ? ORDER by (drink)",
                            session["user_id"])

    if request.method == "POST":

        # Check submit value add
        if request.form['submit'] == 'add':

            drink_check = db.execute("SELECT * FROM inventory WHERE user_id = ? AND drink = ?", session["user_id"], request.form.get("drink_add"))

            if request.form.get("drink_add") == "Select an ingredient":
                flash("Please select a drink to add")
                return render_template("index.html", drinks=drinks, inventory=inventory, stock=inventory)

            elif len(drink_check) != 0:
                flash("Drink already in your stock")
                return render_template("index.html", drinks=drinks, inventory=inventory, stock=inventory)

            else:
                db.execute("INSERT INTO inventory (user_id, drink) VALUES (?, ?)",
                        session["user_id"], request.form.get("drink_add"))
                return redirect("/")


        # Check submit value remove
        if request.form['submit'] == 'remove':

            if request.form.get("drink_remove") == "Select an ingredient":
                flash("Please select a drink to remove")
                return render_template("index.html", drinks=drinks, inventory=inventory, stock=inventory)

            else:
                db.execute("DELETE FROM inventory WHERE user_id = ? AND drink = ?", session["user_id"], request.form.get("drink_remove"))
                return redirect("/")


    return render_template("index.html", drinks=drinks, inventory=inventory, stock=inventory)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check submit value login
        if request.form['submit'] == 'submit_login':

            # Check empty usernarme in login
            if not request.form.get("username"):
                flash("Please Inform username for login")
                return render_template("login.html")

            # Check empty password in login
            elif not request.form.get("password"):
                flash("Please Inform password")
                return render_template("login.html")

            elif checkchars(request.form.get("username")) == True:
                flash("An especial and non valid character was identified")
                return render_template("login.html")

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                flash("Invalid username and/or password")
                return render_template("login.html")

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

        # Check submit value register
        elif request.form['submit'] == 'submit_register':

            username = request.form.get("username_register")
            password = request.form.get("password_register")
            confirmation = request.form.get("confirmation_register")


            rows = db.execute("SELECT * FROM users WHERE username = ?", username)

            # Ensure the username was submitted
            if not username:
                flash("Inform new username to register")
                return render_template("login.html")

            elif checkchars(username) == True:
                flash("An especial and non valid character was identified")
                return render_template("login.html")

            # Ensure the username doesn't exists
            elif len(rows) != 0:
                flash("Username already exist, please choose another username")
                return render_template("login.html")

            # Ensure password was submitted
            elif not password:
                flash("Please inform a password for your user")
                return render_template("login.html")

            # Ensure confirmation password was submitted
            elif not confirmation:
                flash("Please confirm you password")
                return render_template("login.html")

            # Ensure passwords match
            elif password != confirmation:
                flash("Password and password confirmation must be the same")
                return render_template("login.html")

            # Generate the hash of the password
            hash = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=8)

            # Insert the new user
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?) ", username, hash,)

            # Remember which user has logged in
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/cocktailmaker", methods=["GET", "POST"])
@login_required
def cocktailmaker():
    """Cocktail Maker page"""

    inventory = db.execute("SELECT drink from inventory WHERE user_id = ? ORDER by (drink)", session["user_id"])

    if request.method == "POST":
        ingredient = request.form.get("ingredient")
        if ingredient == None or ingredient == "Select an ingredient":
            flash("Please Select an Ingredient")
            return render_template("cocktailmaker.html", inventory=inventory, ingredient=ingredient)

        else:
            cocktails = db.execute("SELECT name FROM cocktails WHERE recipe LIKE ? ", "%" + ingredient + "%")
            return render_template("cocktailmaker.html", inventory=inventory, ingredient=ingredient, cocktails=cocktails)

        request.form.ger("cocktailselected")

    return render_template("cocktailmaker.html", inventory=inventory)

@app.route("/recipe", methods=["GET", "POST"])
@login_required
def recipe():
    """Show choosen cocktail recipe"""

    selected_recipe = request.args.get('type')

    recipe_row = db.execute(" SELECT * FROM cocktails WHERE name= ? ", selected_recipe)
    c_name = recipe_row[0]['name']
    txt_recipe = str(recipe_row[0]['recipe'])
    c_recipe = txt_recipe.split(";")
    c_story = recipe_row[0]['story']

    return render_template("recipe.html", name=c_name, recipe=c_recipe, story=c_story)