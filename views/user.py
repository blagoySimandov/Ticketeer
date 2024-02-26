from flask import (
    Blueprint, g, render_template, request, session, url_for
)
from ..database import get_db,close_db
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile/<id>', methods=['GET', 'POST'])
def profile(id):
    db = get_db()
    user = db.execute(""" SELECT * from users where id = ? """,(id,)).fetchone()
    return render_template('user/profile.html',user=user)
