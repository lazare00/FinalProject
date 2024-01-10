from flask import Flask, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddWorkForm, RegisterForm, EditWorkForm, LoginForm, AddCommentForm
from extensions import app, db
from models import Work, User, Comment


@app.route("/")
def home():
    works = Work.query.all()
    return render_template("index.html", works=works)


@app.route("/search/<string:name>")
def search(name):
    works = Work.query.filter(Work.name.ilike(f"%{name}%"))
    return render_template("search_results.html", works=works)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/view_image/<int:work_id>", methods=["GET", "POST"])
def view_image(work_id):
    work = Work.query.get(work_id)

    if not work:
        return render_template("404.html")

    form = AddCommentForm()

    if form.validate_on_submit():
        new_comment = Comment(user_id=current_user.id, work_id=work.id, text=form.text.data)
        new_comment.create()

        flash("კომენტარი დაემატა")
        return redirect(url_for('view_image', work_id=work.id))

    comments = db.session.query(Comment, User).join(User).filter(Comment.work_id == work.id).all()

    return render_template("work.html", work=work, form=form, comments=comments)


@app.route("/add_work", methods=["GET", "POST"])
@login_required
def add_work():

    form = AddWorkForm()

    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))

        new_work = Work(name=form.name.data, person=form.person.data, img=filename)
        new_work.create()

        flash("პროდუქტი დაემატა")
        return redirect("/")
    else:
        print(form.errors)

    return render_template("add_work.html", form=form)



@app.route("/edit_work/<int:work_id>", methods=["GET", "POST"])
@login_required
def edit_work(work_id):
    if current_user.role != "admin":
        return redirect("/")

    work = Work.query.get(work_id)
    if not work:
        return render_template("404.html")

    form = EditWorkForm(name=work.name, person=work.person)

    if form.validate_on_submit():
        work.name = form.name.data
        work.person = form.person.data

        if form.img.data:
            file = form.img.data
            filename = file.filename
            file.save(path.join(app.root_path, 'static', filename))
            work.img = filename

        work.save()
        return redirect("/")

    return render_template("edit_work.html", form=form)


@app.route("/delete_work/<int:work_id>")
@login_required
def delete_work(work_id):
    if current_user.role != "admin":
        return redirect("/")

    work = Work.query.get(work_id)
    if not work:
        return render_template("404.html")

    work.delete()

    flash("პროდუქტი წაიშალა")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash("სახელი უკვე გამოყენებულია")
        else:
            user = User(username=form.username.data, password=form.password.data)
            user.create()
            flash("თქვენ წარმატებით გაიარეთ რეგისტრაცია")
            return redirect("/")

    print("form.errors")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტირიზაცია")
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("წარმატებულად გამოხვედით აქოუნტიდან")
    return redirect("/")


