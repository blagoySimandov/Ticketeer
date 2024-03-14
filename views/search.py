from flask import (
    Blueprint,url_for,g,session,request,redirect
)
from ..utils import render_with_user
from ..models.ticket import Ticket
from ..models.user import User
from ..database import get_db,close_db
from ..forms.search import SearchForm
bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/tickets', methods=['GET', 'POST'])
def tickets():
    page_size = 3
    page = int(request.args.get('page',1))-1
    form = SearchForm(request.form)
    order = form.order.data if form.order.data != None else 'Price Ascending'
    t_type = form.type.data if form.type.data != 'None' else None
    text = form.search.data if form.search.data != '' else None
    
    db = get_db()
    tickets,count = Ticket.fetch_tickets(db,page,page_size,order,text,t_type)

    close_db()
    for t in tickets:
        print(t.price)
    return render_with_user('search/tickets.html',tickets=tickets,search=form,current_page=page+1, total_pages=-(count//-page_size),count=count)#ceil divison
