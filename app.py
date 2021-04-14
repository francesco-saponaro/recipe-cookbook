import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo, pymongo
from flask_paginate import Pagination
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

# Import Mongo, Mongo database and secret key from env.py
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Create instance of Pymongo with flask as argument
mongo = PyMongo(app)

# Home page
@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    # Pagination:
    # Grab recipes from collection sorted by likes
    recipes = mongo.db.recipes.find()
    # Set page variable needed for pagination
    page = request.args.get('page', 1, type=int)
    # Set amount of recipes to show per page
    per_page = 10
    # Set how many recipes to skip each page by multiplying,
    # recipes per page per current page - 1
    offset = per_page * (page - 1)
    # Apply the per page limit and the offset to the recipes collection
    recipe_page = recipes.skip(offset).limit(per_page)
    # Pagination variable from Flask paginate, it holds the page variable,
    # the length of whole recipe collection and the record name which,
    # should be the name of whatever items are being paginated
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')                       

    # Check if the user is logged in by checking if a session (cookie)
    # has been created for it.
    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("index.html", recipe_page=recipe_page, pagination=pagination, 
                                session_user_id=session_user_id)
    else:
        return render_template("index.html", recipe_page=recipe_page, pagination=pagination)


@app.route("/filter_search", methods=['GET','POST'])
def filter_search():
    # Grab collections from DB in order to populate filter fields
    meal_types = mongo.db.meal_types.find()
    difficulties = mongo.db.difficulties.find()
    prep_times = mongo.db.prep_times.find()
    calories = mongo.db.calories.find()
    dietary_requirements = mongo.db.dietary_requirements.find()
    allergens = mongo.db.allergens.find()
    countries = mongo.db.countries.find().sort("country", 1)

    return render_template("filter_search.html", meal_types=meal_types, difficulties=difficulties, 
    prep_times=prep_times, calories=calories, dietary_requirements=dietary_requirements,
    allergens=allergens, countries=countries)


@app.route("/filter_results", methods=['GET','POST'])
def filter_results():
    # Get values from filter form aside from allergens and 
    # dietary requirements which have a multiple option.
    # Get value from the search query form, search index has been set up
    # on the recipes collection to only find recipes by name or ingredients. 
    # You need to use method="GET" on the form so the form passes the query 
    # into the args, and then in the route, use request.args.get("query") and 
    # not request.form.get - so the query is gotten from the args, 
    # and is kept when you browse pages.
    recipe = {
        "meal_type": request.args.get("meal_types"),
        "difficulty": request.args.get("difficulties"),
        "prep_time": request.args.get("prep_times"),
        "calorie_amount": request.args.get("calories"),
        "is_high_protein": request.args.get("is_high_protein"),
        "country": request.args.get("countries")
    }

    # Add values to the final results object as long as
    # a value has been chosen.
    final_results = {}
    for key, value in recipe.items():
        if value != None:
            final_results.update({key: value})

    # If one or more allergens have been selected 
    # from the list, add all non selected items in the list to the 
    # final results object, as user will choose what they are 
    # in fact allergic too and therefore cannot eat.
    allergens = request.args.getlist("allergens")
    if allergens != []:
        final_results.update({"allergen": {"$nin": allergens}})

    # If one or more dietary_requirements have been selected 
    # from the list, add them to the final results object. 
    diet = request.args.getlist("dietary_requirements")
    if diet != []:
        final_results.update({"dietary_requirement": {"$in": diet}})

    # If a recipe name has been added in the search query
    # add it to the final results object.
    query = request.args.get("recipe_name").lower()
    if query:    
        final_results.update({"$text": {"$search": query}})

    # If an ingredient name has been added in the search query
    # add it to the final results object.
    ingredient = request.args.get("ingredient_name").lower()
    if ingredient:    
        final_results.update({'ingredient.ingredient_name': 
                             {"$regex" : ".*" + ingredient + ".*"}})
        
    # If final results object is not empty, as in if the user chose
    # any option from any field to filter by, find a recipe that
    # matches the final results object. Else redirect user to Home 
    # page which contains all recipes, which is the same as not 
    # filtering by anything.
    if final_results != {}:
        recipes = list(mongo.db.recipes.find(final_results))
    else:
        flash("No filters selected")
        return redirect(url_for("get_recipes"))
    
    # Pagination
    recipes = mongo.db.recipes.find(final_results)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')

    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])
    
        return render_template("filter_results.html", recipe_page=recipe_page,
        pagination=pagination, final_results=final_results,session_user_id=session_user_id)
    else:
        return render_template("filter_results.html", recipe_page=recipe_page,
        pagination=pagination, final_results=final_results)


@app.route("/by_country")
def by_country():
    # Get countries from their collection in ascending order, and 
    # all recipes in order to populate page.
    countries = mongo.db.countries.find().sort("country", 1)
    recipes = list(mongo.db.recipes.find())

    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("by_country.html", recipes=recipes,
        countries=countries, session_user_id=session_user_id)
    else:
        return render_template("by_country.html", recipes=recipes,
        countries=countries)


@app.route("/starters")
def starters():
    # Get all recipes in order to populate page
    meal_types = mongo.db.meal_types.find()
    # Pagination
    recipes = mongo.db.recipes.find({"meal_type": "Starter"})
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')

    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("starters.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types, session_user_id=session_user_id)
    else:
        return render_template("starters.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types)


@app.route("/lunch")
def lunch():
    # Get all recipes in order to populate page
    meal_types = mongo.db.meal_types.find()
    # Pagination
    recipes = mongo.db.recipes.find({"meal_type": "Lunch"})
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')

    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("lunch.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types, session_user_id=session_user_id)
    else:
        return render_template("lunch.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types)


@app.route("/brunch")
def brunch():
    # Get all recipes in order to populate page
    meal_types = mongo.db.meal_types.find()
    # Pagination
    recipes = mongo.db.recipes.find({"meal_type": "Brunch"})
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')

    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("brunch.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types, session_user_id=session_user_id)
    else:
        return render_template("brunch.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types)


@app.route("/dinner")
def dinner():
    # Get all recipes in order to populate page
    meal_types = mongo.db.meal_types.find()
    # Pagination
    recipes = mongo.db.recipes.find({"meal_type": "Dinner"})
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')

    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("dinner.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types, session_user_id=session_user_id)
    else:
        return render_template("dinner.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types)


@app.route("/desserts")
def desserts():
    # Get all recipes in order to populate page
    meal_types = mongo.db.meal_types.find()
    # Pagination
    recipes = mongo.db.recipes.find({"meal_type": "Dessert"})
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')
    
    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("desserts.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types, session_user_id=session_user_id)
    else:
        return render_template("desserts.html", recipe_page=recipe_page,
        pagination=pagination, meal_types=meal_types)


@app.route("/vegan")
def vegan():
    # Get all recipes that have "Vegan" as a dietary requirement 
    # in order to populate page.
    recipes = mongo.db.recipes.find({"dietary_requirement": "Vegan"})
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = per_page * (page - 1)
    recipe_page = recipes.skip(offset).limit(per_page)
    pagination = Pagination(page=page, total=recipes.count(),
                            record_name='recipes')
   
    if "user_session" in session:
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])

        return render_template("vegan.html", recipe_page=recipe_page,
        pagination=pagination, session_user_id=session_user_id)
    else:
        return render_template("vegan.html", recipe_page=recipe_page,
        pagination=pagination)


@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if method is POST, which it will be once the 
    # form has been sent successfully.
    if request.method == "POST":
        # Check if username already exist in database
        existing_user = mongo.db.users.find_one({"username": 
                                                 request.form.get("username").lower()})

        # If so reload page and let them know.
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # This acts as the else statement.
        # Else add form details inside the register dictionary
        # along with an empty lists needed to store the ID of a liked recipe.
        # Password is hashed
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "liked_recipe": []
        }

        # Insert the dictionary in the "users" collection.
        # Put the new user into a session cookie once registered.
        # Let them know the registration was succesful and redirect
        # them to the Home page.
        mongo.db.users.insert_one(register)
        session["user_session"] = request.form.get("username").lower()
        flash("Registration successful")
        return redirect(url_for("get_recipes"))

    # Default GET method if not POST
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if username already exist in database.
        existing_user = mongo.db.users.find_one({"username": 
                                                 request.form.get("username").lower()})

        if existing_user:
            # Check if the input password match the existing user password, if so start a session
            # redirect them to Home page and welcome them.
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user_session"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username").capitalize()))
                return redirect(url_for("get_recipes"))
            # If invalid password match, redirect user to log in page
            else:
                flash("Incorrect username or password")
                return redirect(url_for("login"))
        # If username doesn't exist, redirect to log in page
        else:
            flash("Incorrect username or password")
            return redirect(url_for("login"))

    # Default GET method if not POST
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    your_recipes = request.args.get("your_recipes", None)
    your_favourites = request.args.get("your_favourites", None)

    # Check if a user is logged in
    # Defensive programming
    try:
        if session["user_session"] == username:
            if your_recipes == "your_recipes":
                # Check if the logged in user matches the url's username, this
                # is to prevent other users copying other users url to access
                # their profile.
                # Defensive programming
                if session["user_session"] == username:
                    # Grab the session user's username from mongoDB to populate page header
                    username = mongo.db.users.find_one({"username": 
                                                        session["user_session"]})["username"]

                    # Pagination
                    # Grab all recipes created by the user to populate the page
                    recipes = mongo.db.recipes.find({"created_by": session["user_session"]})
                    page = request.args.get('page', 1, type=int)
                    per_page = 10
                    offset = per_page * (page - 1)
                    recipe_page = recipes.skip(offset).limit(per_page)
                    pagination = Pagination(page=page, total=recipes.count(),
                                            record_name='recipes')

                    # Grab session user's id to check if he has liked the recipe
                    session_user = mongo.db.users.find_one({"username": 
                                                            session["user_session"]})
                    session_user_id = str(session_user["_id"])

                    return render_template("profile.html", username=username, recipe_page=recipe_page,
                    pagination=pagination, session_user_id=session_user_id, your_recipes=your_recipes)
                else:
                    return redirect(url_for("get_recipes"))
                    
            elif your_favourites == "your_favourites":
                # Check if the logged in user matches the url's username, this
                # is to prevent other users copying other users url to access
                # their profile.
                # Defensive programming
                if session["user_session"] == username:
                    session_user = mongo.db.users.find_one({"username": 
                                                            session["user_session"]})
                    session_user_id = str(session_user["_id"])

                    # Grab the session user's username from mongoDB to populate page header
                    username = mongo.db.users.find_one({"username": 
                                                         session["user_session"]})["username"]

                    # Pagination
                    # Find all recipes liked by the user through the user ID, which is added to the 
                    # recipes "user_like" field onclick.
                    # They will be needed to populate page with all liked recipes
                    liked_recipes = mongo.db.recipes.find({"user_like": session_user_id})
                    page = request.args.get('page', 1, type=int)
                    per_page = 10
                    offset = per_page * (page - 1)
                    recipe_page = liked_recipes.skip(offset).limit(per_page)
                    pagination = Pagination(page=page, total=liked_recipes.count(),
                                            record_name='recipes')

                    return render_template("profile.html", username=username, recipe_page=recipe_page,
                    pagination=pagination, session_user_id=session_user_id, your_favourites=your_favourites)
                else:
                    return redirect(url_for("get_recipes"))
            else:
                return render_template("profile.html", username=username)
        else:
            return redirect(url_for("get_recipes"))
    except KeyError:
        return redirect(url_for("get_recipes"))


@app.route("/logout")
def logout():
    # Remove user from session cookies and redirect to 
    # log in page.
    flash("You have been logged out")
    session.pop("user_session")
    
    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    try:
        # Defensive programming
        if session["user_session"]:
            if request.method == "POST":
                # Grab all names, quantity and unit for each ingredient
                # filled in form to be added in their own dictionary.
                names = request.form.getlist("ingredient_name")
                quantities = request.form.getlist("quantity")
                units = request.form.getlist("unit")

                # Initialize ingredients list to which add all ingredient dictionaries
                ingredients = []

                # Initialize ingredient dictionaries to go inside ingredients list
                ingredientdict = {}

                # Iterate by the names list length and for each iteration add into 
                # a dictionary containing that iteration of names, quantity and units.
                for i in range(len(names)):
                    ingredientdict = { "ingredient_name": names[i].lower(),
                                    "quantity": quantities[i],
                                    "unit": units[i]
                                    }    
                    # Append each dictionary to ingredients list, which in turn 
                    # will be passed inside the recipe dictionary.
                    ingredients.append(ingredientdict)
                
                # Dictionary with all values taken from form, 
                # to be inserted in the mongodb "recipes" collection.
                recipe = {
                    # Grab all values through the form's "name" parameter
                    "recipe_name": request.form.get("recipe_name").lower(),
                    "meal_type": request.form.get("meal_types"),
                    "difficulty": request.form.get("difficulties"),
                    "prep_time": request.form.get("prep_times"),
                    "calorie_amount": request.form.get("calories"),
                    "dietary_requirement": request.form.getlist("dietary_requirements"),
                    "allergen": request.form.getlist("allergens"),
                    "serving": request.form.get("servings"),
                    "is_high_protein": request.form.get("is_high_protein"),
                    "country": request.form.get("countries").lower(),
                    "ingredient": ingredients,
                    "description": request.form.get("description"),
                    "recipe_image_url": request.form.get("recipe_image_url"),
                    # Empty lists and integers values to store user likes, comments and amounts
                    "user_like": [],
                    "user_likes": int(0),
                    "comments_count": int(0),
                    # Grab this value from user in session
                    "created_by": session["user_session"]
                }

                # Grab all added ingredient names from form 
                ingredient_list = request.form.getlist("ingredient_name")
                # Loop through ingredients in form and for each, if not already in ingredients
                # collection, add them to it.
                for ingredient in ingredient_list:
                    existing_ingredient = mongo.db.ingredients.find_one({"ingredient_name": 
                                                                         ingredient.lower()})
                    if not existing_ingredient:
                        mongo.db.ingredients.insert_one({"ingredient_name": ingredient.lower()})

                # Check if country already exist in database and if not 
                # already in database, and country field is not empty, grab country 
                # from form and insert it (in lowercase) in the mongodb "countries" collection.
                country = request.form.get("countries")
                existing_country = mongo.db.countries.find_one({"country": 
                                                                request.form.get("countries").lower()})
                if not existing_country and country != "":
                    mongo.db.countries.insert_one({"country": request.form.get("countries").lower()})

                # Insert recipe dictionary in in the mongodb "recipes" collection and
                # redirect to home page once recipe submitted.
                mongo.db.recipes.insert_one(recipe)
                flash("Recipe successfully added")

                return redirect(url_for("get_recipes"))

            # Grab all collections to populate form's select fields
            meal_types = mongo.db.meal_types.find()
            difficulties = mongo.db.difficulties.find()
            prep_times = mongo.db.prep_times.find()
            calories = mongo.db.calories.find()
            dietary_requirements = mongo.db.dietary_requirements.find()
            allergens = mongo.db.allergens.find()
            servings = mongo.db.servings.find()
            return render_template("add_recipe.html", meal_types=meal_types, difficulties=difficulties,
            prep_times=prep_times, calories=calories, dietary_requirements=dietary_requirements,
            allergens=allergens, servings=servings)
            
    # If user not logged in run KeyError, which is raised when 
    # a mapping (dictionary) key is not found in the set of existing keys.
    # Redirect user to log in page
    except KeyError:
        return redirect(url_for("get_recipes"))


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    try:
        # Grab current recipe and username of logged in user, and check
        # if there a user logged in and if its username matches the
        # "created_by" field of the recipe being edited. If so edit 
        # recipe, else redirect to Home page
        # Defensive programming
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        username = mongo.db.users.find_one({"username": session["user_session"]})["username"]

        if session["user_session"] and username == recipe["created_by"]:
            if request.method == "POST":
                # Grab all names, quantity and unit for each ingredient
                # filled in form to be added in their own dictionary.
                names = request.form.getlist("ingredient_name")
                quantities = request.form.getlist("quantity")
                units = request.form.getlist("unit")

                # Initialize ingredients list to which add all ingredient dictionaries
                ingredients = []

                # Initialize ingredient dictionaries to go inside ingredients list
                ingredientdict = {}

                # Iterate by the names list length and for each iteration add into 
                # a dictionary containing that iteration of names, quantity and units.
                for i in range(len(names)):
                    ingredientdict = { "ingredient_name": names[i].lower(),
                                    "quantity": quantities[i],
                                    "unit": units[i]
                                    }
                    # Append each dictionary to ingredients list, which in turn 
                    # will be passed inside the recipe dictionary.
                    ingredients.append(ingredientdict)

                # Get this non editable values from original recipe, in order to be added in 
                # the submit (edited) dictionary.
                recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
                user_like = recipe["user_like"]
                user_likes = recipe["user_likes"]
                comments_count = recipe["comments_count"]

                # Dictionary with all values taken from form, plus non editable
                # values, to be inserted in the mongodb "recipes" collection.
                submit = {
                    "recipe_name": request.form.get("recipe_name").lower(),
                    "meal_type": request.form.get("meal_types"),
                    "difficulty": request.form.get("difficulties"),
                    "prep_time": request.form.get("prep_times"),
                    "calorie_amount": request.form.get("calories"),
                    "dietary_requirement": request.form.getlist("dietary_requirements"),
                    "allergen": request.form.getlist("allergens"),
                    "serving": request.form.get("servings"),
                    "is_high_protein": request.form.get("is_high_protein"),
                    "country": request.form.get("countries").lower(),
                    "ingredient": ingredients,
                    "description": request.form.get("description"),
                    "recipe_image_url": request.form.get("recipe_image_url"),
                    "user_like": user_like,
                    "user_likes": user_likes,
                    "comments_count": comments_count,
                    # Grab this value from logged in user
                    "created_by": session["user_session"]
                }

                # Grab all added ingredient names from form 
                ingredient_list = request.form.getlist("ingredient_name")
                # Loop through ingredients in form and for each, if not already in ingredients
                # collection, add them to it.
                for ingredient in ingredient_list:
                    existing_ingredient = mongo.db.ingredients.find_one({"ingredient_name": 
                                                                        ingredient.lower()})
                    if not existing_ingredient:
                        mongo.db.ingredients.insert_one({"ingredient_name": ingredient.lower()})

                # Check if country already exist in database and if not already in 
                # database, and country field is not empty, grab country from form 
                # and insert it (in lowercase) in the mongodb "countries" collection.
                country = request.form.get("countries")
                existing_country = mongo.db.countries.find_one({"country": 
                                                                request.form.get("countries").lower()})
                if not existing_country and country != "":
                    mongo.db.countries.insert_one({"country": request.form.get("countries").lower()})

                # Update dictionary in mongodb database. "update" method takes two parameters, 
                # first is the dictionary to be updated and the second is the updated dictionary.
                # We find the dictionary to be updated through the recipe.id of the current recipe
                mongo.db.recipes.update({"_id":ObjectId(recipe_id)}, submit)
                flash("Recipe successfully updated")

                # Redirect to home page once recipe updated
                return redirect(url_for("get_recipes"))
            
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
            return render_template("edit_recipe.html", recipe=recipe, meal_types=meal_types,
            difficulties=difficulties, prep_times=prep_times, calories=calories,
            dietary_requirements=dietary_requirements, allergens=allergens, servings=servings)
        else:
            flash("You can only edit your own recipes")
            return redirect(url_for("get_recipes"))

    except KeyError:
        flash("You need to be logged in to edit a recipe")
        return redirect(url_for("get_recipes"))


@app.route("/recipe_page/<recipe_id>")
def recipe_page(recipe_id):
    # Grab current recipe to populate page
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    # Grab comments to populate page
    comments = mongo.db.comments.find()

    if "user_session" in session:
        # Grab user's username to check if comments belong to him
        username = mongo.db.users.find_one({"username": 
                                             session["user_session"]})["username"]
        # Grab session user's id to check if he has liked the recipe
        session_user = mongo.db.users.find_one({"username": session["user_session"]})
        session_user_id = str(session_user["_id"])
        
        return render_template("recipe_page.html", recipe=recipe, 
        session_user_id=session_user_id, session_user=session_user, comments=comments, username=username)
    else:
        return render_template("recipe_page.html", recipe=recipe, comments=comments)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    # Grab the current recipe and all comments with current
    # recipe id and delete them
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    comment = mongo.db.comments.find({"recipe_id": ObjectId(recipe_id)})
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    for i in comment:
        mongo.db.comments.remove(i)
    # Remove deleted recipe from users likes and comments fields, if any
    mongo.db.users.update_many({},
                               {"$pull": {"liked_recipe": ObjectId(recipe_id)}})

    # Redirect user to Home page
    flash("Recipe successfully deleted")
    return redirect(url_for("get_recipes"))


@app.route("/like_recipe/<recipe_id>", methods=["GET", "POST"])
def like_recipe(recipe_id):
    # Liking a recipe will be executed through a form
    if request.method == "POST":
        # Defensive programming
        if session["user_session"]:
            # The session user ID is to be added in liked recipe document
            session_user = mongo.db.users.find_one({"username": session["user_session"]})
            session_user_id = str(session_user["_id"])

            # Grab value from form
            check_favourite = request.form.get("check-favourite")
            
            # If value is true (like) and recipe ID is not already in user liked_recipe field,
            # add the recipe ID in the user liked_recipe field, add the user ID in the
            # recipe's user_like field, and increase recipe's user_likes field by 1.
            # Redirect user to liked recipe page on each like
            if check_favourite == "true":
                if ObjectId(recipe_id) not in session_user["liked_recipe"]:
                    mongo.db.users.update({"username": session["user_session"]},
                                          {"$push": {"liked_recipe": ObjectId(recipe_id)}})
                    mongo.db.recipes.update({"_id": ObjectId(recipe_id)},
                                            {"$push": {"user_like": session_user_id}})
                    mongo.db.recipes.update({"_id": ObjectId(recipe_id)},
                                            {"$inc": {"user_likes": 1}})
                    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

                    # Return the user to the current page
                    return redirect(request.referrer)

            # If value is false (unlike) and recipe ID is in user liked_recipe field,
            # remove the recipe ID in the user liked_recipe field, remove the user ID in the
            # recipe's user_like field, and decrease recipe's user_likes field by 1.
            # Redirect user to Home page on each unlike
            elif check_favourite == "false":
                if ObjectId(recipe_id) in session_user["liked_recipe"]:
                    mongo.db.users.update({"username": session["user_session"]},
                                          {"$pull": {"liked_recipe": ObjectId(recipe_id)}})
                    mongo.db.recipes.update({"_id": ObjectId(recipe_id)},
                                            {"$pull": {"user_like": session_user_id}})
                    mongo.db.recipes.update({"_id": ObjectId(recipe_id)},
                                            {"$inc": {"user_likes": -1}})

                    # Return the user to the current page
                    return redirect(request.referrer)

    return redirect(url_for("get_recipes"))


@app.route("/comments/<recipe_id>", methods=["GET", "POST"])
def comments(recipe_id):
    # Commenting a recipe will be executed through a form
    if request.method == "POST":
        # Defensive programming
        if session["user_session"]:
            session_user = mongo.db.users.find_one({"username": session["user_session"]})

            # Get comment from form 
            # Add the commented recipe ID, the user's username and the comment in the comments
            # collection, and increase commented recipe's comments_count field by 1 
            # Redirect user to recipe page
            comment = request.form.get("comment")
            mongo.db.comments.insert_one({"recipe_id": ObjectId(recipe_id),
                                          "user": session_user["username"],
                                          "comment": comment})
            mongo.db.recipes.update({"_id": ObjectId(recipe_id)},
                                    {"$inc": {"comments_count": 1}})
            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

            return render_template("recipe_page.html", recipe=recipe)

    return render_template("recipe_page.html", recipe=recipe)


@app.route("/delete_comment/<recipe_id>/<comment_id>")
def delete_comment(recipe_id, comment_id):
    # Grab the targeted comment and delete it
    mongo.db.comments.remove({"_id": ObjectId(comment_id)})
    # Decrease recipe's comment's count field by 1.
    mongo.db.recipes.update({"_id": ObjectId(recipe_id)},
                            {"$inc": {"comments_count": -1}})

    # Redirect the user to the current page
    flash("Comment successfully deleted")
    return redirect(request.referrer)


@app.route('/dashboard')
def dashboard():
    # Iterate through desired category and for each iteration create
    # a dict with the iteration and the count of recipes matching
    # that iteration as values, then append dictionaries to a list
    # as AMCharts works with lists of dictionaries.

    # To populate "Recipes by Meal types" chart
    meal_types_list = []
    meal_types_dict = {}
    meal_types = mongo.db.meal_types.find()
    for meal_type in meal_types:
        meal_types_dict = {'meal_type': meal_type['meal_type'],
                           'amount':mongo.db.recipes.find({'meal_type': 
                                                            meal_type["meal_type"]}).count()}
        meal_types_list.append(meal_types_dict)

    # To populate "Recipes by Difficulty" chart
    difficulties_list = []
    difficulties_dict = {}
    difficulties = mongo.db.difficulties.find()
    for difficulty in difficulties:
        difficulties_dict = {'difficulty': difficulty['difficulty'],
                             'amount':mongo.db.recipes.find({'difficulty': 
                                                             difficulty['difficulty']}).count()}
        difficulties_list.append(difficulties_dict)

    # To populate "Recipes by User" chart
    user_list = []
    user_dict = {}
    users = mongo.db.users.find()
    for user in users:
        user_dict = {'user': user['username'],
                     'amount':mongo.db.recipes.find({'created_by': 
                                                     user['username']}).count()}
        user_list.append(user_dict)

    # To populate "Recipes by Country" chart
    countries_list = []
    countries_dict = {}
    countries = mongo.db.countries.find()
    for country in countries:
        countries_dict = {'country': country["country"].capitalize(),
                          'amount':mongo.db.recipes.find({'country': 
                                                           country["country"]}).count()}
        countries_list.append(countries_dict)

    # To populate "Recipes by Dietary Requirement" chart
    diet_list = []
    diet_dict = {}
    diets = mongo.db.dietary_requirements.find()
    for diet in diets:
        diet_dict = {'dietary_requirement': diet["dietary_requirement"],
                     'amount':mongo.db.recipes.find({'dietary_requirement': 
                                                      diet["dietary_requirement"]}).count()}
        diet_list.append(diet_dict)
    
    
    return render_template('dashboard.html', meal_types_list=meal_types_list, 
    difficulties_list=difficulties_list,user_list=user_list, countries_list=countries_list, 
    diet_list=diet_list)


# error handler is a built in Flask function that returns a response 
# when a type of error is raised
# error 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('not_found.html', error=error), 404


# error 500 
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_error.html', error=error), 500
   
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)