from datetime import datetime
import time
from fileinput import filename
from os import path
from hashlib import sha256
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, g, render_template, request, session, url_for
)
from ..utils import render_with_user
from shutil import copyfileobj
from .auth import login_required
from ..forms.ticket import TicketForm
from ..models.ticket import Ticket
from ..models.history import History, ActionType
from ..database import get_db, close_db,decimal_to_int
bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    form = TicketForm()
    if form.validate_on_submit():
        seller_id =  g.user
        event_date = form.eventDate.data
        event_time = form.eventTime.data
        event_datetime = datetime(event_date.year, event_date.month, event_date.day, 
                          event_time.hour, event_time.minute, event_time.second)
        big_int_price = decimal_to_int(form.price.data)
        f = form.ticketPDF.data 
        timestamp = str(int(time.time()))#timestamp is used so that if two users upload a file with the same 
                                         #name the hashes would still be different.
        hashed_f_name = sha256((f.filename+timestamp).encode()).hexdigest()
        save_file(f,'static/tickets',hashed_f_name,)
        ticket = Ticket(
            event_name=form.eventName.data,
            event_date=event_datetime,
            venue=form.venue.data,
            ticket_type=form.ticketType.data,
            price=big_int_price,
            quantity=form.quantity.data,
            seat_number=form.seatNumber.data,
            seller_id=seller_id,
            ticket_filename=hashed_f_name
        )
        history= History(g.user,action=ActionType.POST_TICKET,ticket_id=ticket.id)#on creation ticket.id is generated as uuid
        db = get_db()
        ticket.insert_ticket(db)
        history.insert_entry(db)
        db.commit()
        close_db()
        return 'Ticket uploaded ;d'
    return render_with_user('post/ticket.html', form=form)

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