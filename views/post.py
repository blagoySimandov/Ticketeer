from datetime import datetime
import uuid

from hashlib import sha256

from flask import (
    Blueprint, g, render_template, request, session, url_for
)



from ..utils import render_with_user,save_file

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
        print(event_time)
        event_datetime = datetime.combine(event_date,event_time)
        big_int_price = decimal_to_int(form.price.data)
        f = form.ticketPDF.data
        hashed_f_name = uuid.uuid4()
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

