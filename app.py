from flask import Flask, render_template, redirect,session,redirect,url_for,g
from flask_session import Session
from app.forms.signup import SignUpForm,LogInForm
from werkzeug.security import generate_password_hash,check_password_hash
from app.database.connections import get_db,close_db
from functools import wraps
from . import app

app.teardown_appcontext(close_db)
@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id",None)
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return view(*args,**kwargs)
    return wrapped_view
@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template("home.html")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form =  SignUpForm()
    if form.validate_on_submit():
        db = get_db()
        hash = generate_password_hash(form.password.data)
        print(hash)
        email_exists = db.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)", (form.email.data,)).fetchone()
        if not email_exists:
            db.execute("INSERT into users (email,password_hash,name) VALUES (?,?,?)",(form.email.data,hash,form.u_name.data))
            db.commit()
            return redirect(url_for("/"))
        form.email.errors.append("This email already exists")
    return render_template("sign-up.html",form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form =  LogInForm()
    if form.validate_on_submit():
        db = get_db()
        hash = db.execute("SELECT password_hash from users WHERE email = ?",(form.email.data,)).fetchone()
        close_db()
        if hash is not None and check_password_hash(hash,form.password.data):
                session['logedin'] = True
                return redirect(url_for("/"))
        form.password.errors.append("Wrong email or password.")
        return render_template("sign-in.html",form=form)
    return render_template("sign-in.html",form=form)
@app.route('/post_ticket', methods=['GET', 'POST'])
@login_required
def post_ticket():
    pass
         

