"""Flask app for Authentication/Authorization."""

from flask import Flask, render_template, redirect, jsonify, request, flash, session
from models import db, connect_db, User, Feedback, bcrypt
from forms import AddUserForm, LoginUserForm, EditFeedbackForm, NewFeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

# db.drop_all()
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():

    """Redirects to /register."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def add_user_form():

    """Instantiates AddUserForm() and displays form on page."""

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        flash("New User created.  Welcome to the Feedback app!")

        return redirect(f'/users/{ new_user.username }')

    else:
        return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    """Shows login form and logs user in when submitted."""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:

            session["username"] = user.username
            flash(f"Welcome, {user.first_name}")
            return redirect(f'/users/{ user.username }')

        else:
            
            form.password.errors = ["Invalid username/password"]

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():

    """Logs user out and redirects to root route."""

    session.pop('username')

    flash("You have successfully logged out.")
    return redirect("/")


# ***************************************************************************
# User routes 
# ***************************************************************************


@app.route("/users/<username>")
def show_secret_page(username):

    """Displays user profile page."""

    user = User.query.get_or_404(username)
    
    if "username" not in session:

        flash("You must be logged in to view page.")
        return redirect("/login")

    return render_template("user-profile.html", user=user)



@app.route("/users/<username>/delete", methods=["POST"])
def delete_account(username):

    """Allows user to delete own account."""

    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

# ***************************************************************************
# Feedback routes 
# ***************************************************************************

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    """Displays new feedback form."""

    form = NewFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        if session["username"] == username:
            feedback = Feedback(title=title, content=content, username=username)

            db.session.add(feedback)
            db.session.commit()

            return redirect(f"/users/{ username }")

        else:
            flash("You have to be signed in to add new feedback.")
            return redirect(f"/users/{ username }")

    return render_template("add-feedback.html", form=form)


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):

    """Takes user to a form to edit selected feedback."""

    fb = Feedback.query.get_or_404(feedback_id)
    form = EditFeedbackForm(obj=fb)

    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content = form.content.data

        db.session.add(fb)
        db.session.commit()

        return redirect(f"/users/{ fb.username }")

    return render_template('edit-feedback.html', form=form)


@app.route("/feedback/<feedback_id>/delete", methods=["GET", "POST"])
def delete_feedback(feedback_id):

    """Deletes a single feedback."""

    fb = Feedback.query.get_or_404(feedback_id)

    db.session.delete(fb)
    db.session.commit()

    return redirect(f"/users/{ fb.username }")

