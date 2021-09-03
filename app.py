import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
# Home page
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    # option for user to search for a recipe
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    # option for user to register
    if request.method == "POST":

        # username = request.form.get("username").lower(),
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        print(confirm_password)

        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Password does not match")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into "session" cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Hello, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect username/password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect username/password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if session["user"]:
        # get the session username from the database
        if session["user"] == "admin":
            recipe = mongo.db.recipes.find()
        else:
            # get users recipes from the database
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            user = session.get("user").lower()
            user_recipes = list(
                mongo.db.recipes.find({"created_by": session["user"]})          )
        return render_template(
            "profile.html", recipes=user_recipes, username=username)
    return redirect(url_for("login.html"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have successfully logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    # option for user to create a recipe
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "category_name": request.form.get("category_name"),
            "method": request.form.get("method"),
            "ingredients": request.form.get("ingredients"),
            "created_by": session["user"],
            "recipe_img_url": request.form.get("recipe_img_url"),
            "recipe_url": request.form.get("recipe_img"),
            "serves": request.form.get("serves"),
            "prep_time": request.form.get("prep_time"),
            "serves": request.form.get("serves")
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe successfully added")
        return redirect(url_for("profile", username=session['user']))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("create_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    # option for user to edit a recipe
    if request.method == "POST":
        submit = {
            "recipe_name": request.form.get("recipe_name"),
            "category_name": request.form.get("category_name"),
            "method": request.form.get("method"),
            "ingredients": request.form.get("ingredients"),
            "created_by": session["user"],
            "recipe_img_url": request.form.get("recipe_img_url"),
            "recipe_url": request.form.get("recipe_img"),
            "serves": request.form.get("serves"),
            "prep_time": request.form.get("prep_time"),
            "serves": request.form.get("serves")
        }
        # update edited recipe to the database
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe successfully updated")
        return redirect(url_for("profile", username=session['user']))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories
        )


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    # delete a recipe from the database
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe successfully deleted")
    return redirect(url_for("get_recipes"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        # add a category to the database
        mongo.db.categories.insert_one(category)
        flash("New category added")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        # update category in database
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    # delete category from the database
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("get_categories"))


@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if request.method == "POST":
        # check if email already exists
        existing_email = mongo.db.subscribers.find_one(
            {"email": request.form.get("email")})

        # if existing email
        if existing_email:
            flash("Email already exists")
            return redirect(url_for("get_recipes"))

        # add subscriber to the database
        subscribe = {
            "email": request.form.get("email").lower()
        }

        mongo.db.subscribers.insert_one(subscribe)
        flash("Thank you for subscribing")
    return redirect(url_for("get_recipes"))


@app.route("/full_recipe/<recipe_id>")
# show full recipe to user
def full_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    if not recipe:
        return render_template("/404.html")

    return render_template(
        "full_recipe.html", recipe=recipe)


# show user 404 error page if page does not exist
@app.errorhandler(404)
def error(e):
    return render_template("/404.html"), 404


# Run the application
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # change to False before submitting

