import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("index.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exist in database
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        # this acts as the else statement
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into a session cookie
        session["user_session"] = request.form.get("username").lower()
        flash("Registration successful")
        redirect(url_for("profile", username=session["user_session"]))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exist in database
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            # check if the input password match the existing user password, if so start a session
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user_session"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                redirect(url_for("profile", username=session["user_session"]))
            else:
                # invalid password match, if invalid reidrec the user to log in page
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        
        else:
            # username doesn't exist, therefore flash message and redirect to log in page
            flash("Incorrect username or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from mongoDB
    username = mongo.db.users.find_one({"username": session["user_session"]})["username"]

    if session["user_session"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user_session")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "meal_type": request.form.get("meal_types"),
            "difficulty": request.form.get("difficulties"),
            "prep_time": request.form.get("prep_times"),
            "calorie_amount": request.form.get("calories"),
            "dietary_requirement": request.form.getlist("dietary_requirements"),
            "allergen": request.form.getlist("allergens"),
            "serving": request.form.get("servings"),
            "is_high_protein": request.form.get("is_high_protein"),
            "country": request.form.get("countries"),
            "ingredient": request.form.get("ingredient"),
            "ingredient_quantity": request.form.get("ingredient_quantity"),
            "unit": request.form.get("units"),
            "description": request.form.get("description"),
            "created_by": session["user_session"]

        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe successfully added")
        return redirect(url_for("get_recipes"))

    meal_types = mongo.db.meal_types.find()
    difficulties = mongo.db.difficulties.find()
    prep_times = mongo.db.prep_times.find()
    calories = mongo.db.calories.find()
    dietary_requirements = mongo.db.dietary_requirements.find()
    allergens = mongo.db.allergens.find()
    countries = mongo.db.countries.find().sort("country", 1)
    servings = mongo.db.servings.find()
    units = mongo.db.units.find()
    return render_template("add_recipe.html", meal_types=meal_types, difficulties=difficulties, prep_times=prep_times, calories=calories, dietary_requirements=dietary_requirements, allergens=allergens, servings=servings, units=units)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    meal_types = mongo.db.meal_types.find()
    difficulties = mongo.db.difficulties.find()
    prep_times = mongo.db.prep_times.find()
    calories = mongo.db.calories.find()
    dietary_requirements = mongo.db.dietary_requirements.find()
    allergens = mongo.db.allergens.find()
    countries = mongo.db.countries.find().sort("country", 1)
    servings = mongo.db.servings.find()
    units = mongo.db.units.find()
    return render_template("edit_recipe.html", recipe=recipe, meal_types=meal_types, difficulties=difficulties, prep_times=prep_times, calories=calories, dietary_requirements=dietary_requirements, allergens=allergens, servings=servings, units=units)




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)