from flask import Flask, render_template, redirect,session,redirect,url_for,g
from flask_session import Session
from .models.user import User
from .database import get_db,close_db
from fileinput import filename
from werkzeug.utils import secure_filename
from os import path
from shutil import copyfileobj
def render_with_user(*args, **kwargs):
    if session.get('user_id',None) is not None:
        db = get_db()
        user = User.from_db(db,session['user_id'])
        close_db()
        results = render_template(*args,**kwargs,user=user)
    else:
        results = render_template(*args, **kwargs)
    return results
#save file to local storage
def save_file(file_stream, directory_path, file_name):
    ext = get_file_extension(file_stream)
    file_path = path.join(directory_path, f"{file_name}{ext}")
    with open(file_path, 'wb') as f:
        copyfileobj(file_stream, f)
def get_file_extension(file_stream):
    filename = secure_filename(file_stream.filename)
    _, file_extension = path.splitext(filename)
    return file_extension