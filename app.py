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

# Create instance of Pymongo with flask as argument
mongo = PyMongo(app)

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    # We grab the recipes from mongodb "recipes" collection to populate the page
    recipes = mongo.db.recipes.find()
    return render_template("index.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exist in database
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # This acts as the else statement
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        # Insert the dictionary in the "users" collection
        mongo.db.users.insert_one(register)
        # Put the new user into a session cookie once registered
        session["user_session"] = request.form.get("username").lower()
        flash("Registration successful")
        # Send user to home page once registered 
        return redirect(url_for("get_recipes"))

    # Default GET method if not POST
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username already exist in database
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            # Check if the input password match the existing user password, if so start a session
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user_session"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username").capitalize()))
                # Send user to home page once logged in
                return redirect(url_for("get_recipes"))
            else:
                # If invalid password match, redirect user to log in page
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        
        else:
            # Username doesn't exist, redirect to log in page
            flash("Incorrect username or password")
            return redirect(url_for("login"))

    # Default GET method if not POST
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Grab the session user's username from mongoDB, this will be the argument for our function and therefore our URL, we will use it to welcome the user to the application
    username = mongo.db.users.find_one({"username": session["user_session"]})["username"]
    # Grab the recipes from mongodb "recipes" collection to populate the page
    recipes = mongo.db.recipes.find()

    # Defensive programming
    if session["user_session"]:
        return render_template("profile.html", username=username, recipes=recipes)

    # If not logged in redirect to log in page
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove user from session cookies
    flash("You have been logged out")
    session.pop("user_session")
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # Create the dictionary to be inserted in the mongodb "recipe" collection
        recipe = {
            # Grab all values through the form's "name" parameter
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
            # Grab this value from user in session
            "created_by": session["user_session"]
        }
        # Grab ingredient from form and insert it (in lowercase) in the mongodb "ingredients" collection
        mongo.db.ingredients.insert_one({"ingredient": request.form.get("ingredient").lower()})
        # Grab country from form and insert it (in lowercase) in the mongodb "countries" collection
        mongo.db.countries.insert_one({"country": request.form.get("countries").lower()})
        # Insert dictionary in in the mongodb "recipes" collection
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe successfully added")
        # Redirect to home page once recipe submitted
        return redirect(url_for("get_recipes"))

    # Grab all collections to populate form's select fields
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
    if request.method == "POST":
        # Create the dictionary to be inserted in the mongodb "recipe" collection
        submit = {
            # Grab all values through the form's "name" parameter
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
            # Grab this value from logged in user
            "created_by": session["user_session"]

        }
        # Update dictionary in mongodb database. "update" method takes two parameters, first is the dictionary to be updated and the second is the updated dictionary. We find the dictionary to be updated through the recipe.id coming from the route
        mongo.db.recipes.update({"_id":ObjectId(recipe_id)}, submit)
        flash("Recipe successfully updated")
        # Redirect to home page once recipe updated
        return redirect(url_for("get_recipes"))

    # Grab the recipe through it's "_id" value to populate form's select fields
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    # Grab all collections to populate form's select fields
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


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id":ObjectId(recipe_id)})
    flash("Task successfully deleted")
    return redirect(url_for("get_recipes"))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)