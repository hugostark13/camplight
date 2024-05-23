import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import Search, Add
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

USER_ADDED = "User details added successfully!"
USER_EXIST = "User alredy exists!"
SUCCESS = "success"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/users", methods=["GET", "POST"])
def users():

    all_users = db.session.query(User).all()

    # Add pagination
    page = request.args.get("page", 1, type=int)
    per_page = 3
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(all_users) + per_page - 1) // per_page
    items_on_page = all_users[start:end]
    # End pagiantion

    form = Add()
    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()
        phone = form.phone.data.strip()
        if request.method == "POST":
            new_user = User(
                name=name,
                email=email,
                phone=phone,
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash(USER_ADDED, SUCCESS)
                return redirect(url_for("users"))
            except IntegrityError:
                db.session.rollback()
                flash(USER_EXIST)

    return render_template(
        "users.html",
        items_on_page=items_on_page,
        total_pages=total_pages,
        page=page,
        form=form,
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    form = Search()
    if form.validate_on_submit():
        name = form.name.data.title()
        searched_name = db.session.query(User).filter(User.name == name)
        return render_template("search.html", form=form, users=searched_name)
    return render_template("search.html", form=form)


@app.route("/delete", methods=["GET", "DELETE"])
def delete():
    user_id = request.args.get("id")
    selected_cafe = User.query.get(user_id)
    db.session.delete(selected_cafe)
    db.session.commit()
    return redirect(url_for("users"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
