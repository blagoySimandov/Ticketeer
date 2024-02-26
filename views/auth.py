import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,g
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..database import close_db, get_db
from app.forms.signup import LogInForm, SignUpForm

bp = Blueprint('auth', __name__, url_prefix='/auth')
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(*args,**kwargs)
    return wrapped_view
@bp.route('/signup', methods=['GET', 'POST'])
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
    return render_template("auth/sign-up.html",form=form)
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form =  LogInForm()
    if form.validate_on_submit():
        db = get_db()
        user = db.execute("SELECT id,password_hash from users WHERE email = ?",(form.email.data,)).fetchone()
        close_db()
        if hash is not None and check_password_hash(user["password_hash"],form.password.data):
                session['logedin'] = True
                session['user_id'] = user['id']
                return redirect(url_for("index"))
        form.password.errors.append("Wrong email or password.")
        return render_template("auth/sign-in.html",form=form)
    return render_template("auth/sign-in.html",form=form)
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))