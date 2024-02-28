from flask import Flask, render_template, redirect,session,redirect,url_for,g
from flask_session import Session
from .models.user import User
from .database import get_db,close_db
def render_with_user(*args, **kwargs):
    if session.get('user_id',None) is not None:
        db = get_db()
        user = User.from_db(db,session['user_id'])
        close_db()
        results = render_template(*args,**kwargs,user=user)
    else:
        results = render_template(*args, **kwargs)
    return results