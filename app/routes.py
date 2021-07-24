# -*- coding: utf-8 -*-
from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from datetime import datetime
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, login_required, logout_user

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [{
        "author": {"username": "Jony"},
        "body": "its a butiful gocno"
    },
        {
            "author": {"username": "Alex"},
            "body": "300 baks"
        },
        {
            "author": {"username": "Som"},
            "body": "poshol ty"
        }]
    html_text = render_template("index.html", title="Home", posts=posts)
    return html_text


@app.route("/login", methods={"GET", "POST"})
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash("Ivalid password or login")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if next_page:
            url = next_page
        else:
            url = url_for("index")
        print(url)
        return redirect(url)
    return render_template("login.html", title="Sign in", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are Registered")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test 1"},
        {"author": user, "body": "Test 2"}
    ]
    return render_template("user.html", user=user, posts=posts)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit profile", form=form)

@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} not found")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot follow yoursels")
        return redirect(url_for("user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are following {username}")
    return redirect(url_for("user", username=username))

@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} not found")
        return redirect(url_for("index"))
    if user == current_user:
        flash("You cannot unfollow yoursels")
        return redirect(url_for("user", username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You are unfollowing {username}")
    return redirect(url_for("user", username=username))