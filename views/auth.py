import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,g
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.history import History,ActionType
from ..models.user import User
from ..database import close_db, get_db
from app.forms.auth import LogInForm, SignUpForm

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
        email_exists = db.execute("SELECT EXISTS(SELECT email FROM users WHERE email = ?)", (form.email.data,)).fetchone()[0]
        print(email_exists)
        if not email_exists:
            hash = generate_password_hash(form.password.data)
            user = User(email=form.email.data, password_hash=hash, first_name=form.f_name.data, last_name=form.l_name.data)
            user.register_user(db)#makes database operation and scans the inserted id back into the model.
            history_entry = History(user_id=user.id, action=ActionType.REGISTER, details=f"{user.first_name} joined Ticketeer.")
            history_entry.insert_entry(db)
            db.commit()
            close_db()
            return redirect(url_for("index"))
        close_db()
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