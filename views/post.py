from datetime import datetime
import time
from fileinput import filename
from os import path
from hashlib import sha256
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, g, render_template, request, session, url_for
)
from shutil import copyfileobj
from .auth import login_required
from ..forms.ticket import TicketForm
from ..models.ticket import Ticket
from ..database import get_db, close_db,decimal_to_int
bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/ticket', methods=['GET', 'POST'])
@login_required
def post_ticket():
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
            ticket_pdf_filename=hashed_f_name
        )
        db = get_db()
        insert_ticket(ticket,db)
        close_db()
        return 'Ticket uploaded successfully!'
    return render_template('post/ticket.html', form=form)

def insert_ticket(ticket,db):
    db.execute("""
        INSERT INTO tickets (event_name, event_date, venue, ticket_type, price, quantity, seat_number, seller_id, ticket_pdf_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket.event_name,
        ticket.event_date,
        ticket.venue,
        ticket.ticket_type,
        ticket.price,
        ticket.quantity,
        ticket.seat_number,
        ticket.seller_id,
        ticket.ticket_pdf_filename
    ))
    db.commit()

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