from flask import (
    Blueprint,url_for,g,session,request,redirect
)
import uuid
from ..forms.user import UpdateUserForm
from ..forms.card_details import CardDetails
from ..models.user import User
from ..models.ownership import Ownership
from ..models.ticket import Ticket,sum_prices_of_tickets
from .auth import login_required
from ..views.post import save_file
from ..models.history import History,ActionType
from ..utils import render_with_user,save_file
from ..database import get_db,close_db,int_to_decimal
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    history = None
    if g.user is not None:
        db = get_db()
        history = History.fetch_history(db,g.user)
        close_db()
    return render_with_user('user/profile.html',history=history)
@login_required
@bp.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateUserForm()
    db = get_db()
    userOld = User.from_db(db,user_id=g.user)
    close_db()
    saved_entries = session.get('social_link_entries', {})
    if form.is_submitted():
        if form.social_media_platform.add.data == True:  
                #Adds a social media input field
                platform = form.social_media_platform.data['social_media_platform']
                saved_entries[platform]= ''
                populate_platforms(saved_entries=saved_entries,form=form)
        elif form.save.data == True:
            #Form is submitted and validated. If it is validated it is inserted into the db.
            if form.validate():
                db = get_db()
                user = userOld
                if form.profile_picture.data is not None:
                    f = form.profile_picture.data
                    hashed_f_name = uuid.uuid4()
                    ext = save_file(f,'static/profile_pics',hashed_f_name)
                    user.profile_picture = str(hashed_f_name)+ext
                    print(user.profile_picture)
                
                updated_fields =user.update_from_form(form,request)
                user.update_to_db(db,updated_fields) #makes insert to db
                history = History(id=uuid.uuid4(),user_id=g.user,action=ActionType.UPDATED_PROFILE)
                history.insert_entry(db)
                db.commit()
                close_db()
                del saved_entries
                session.modified=True
                return redirect(url_for('user.profile'))
            populate_platforms(saved_entries=saved_entries,form=form)   
            return render_with_user('user/update.html',form=form)
        else:
            #Removes a social media input field
            relevant_fields = {}
            for key, value in request.form.items():
                if key.startswith(('facebook', 'twitter', 'instagram', 'remove_')):
                    relevant_fields[key] = value
            remove_social_media = None
            for key, value in relevant_fields.items():
                if key.startswith("remove_") and value == "Remove":
                    remove_social_media = key[len("remove_"):] #using len(remove_) so that there is not a magic number injected in.
                    if remove_social_media in saved_entries:
                        saved_entries.pop(remove_social_media)
                    populate_platforms(saved_entries=saved_entries,form=form)
    else:
        form.bio.data = userOld.bio
        form.location.data = userOld.location
        form.phone_number.data = userOld.phone_number
    
    populate_platforms(saved_entries,form)
    return render_with_user('user/update.html',form=form)

def populate_platforms(saved_entries,form): 
    while form.social_link.entries:
        form.social_link.pop_entry()
    for platform in saved_entries:
        new_entry = form.social_link.append_entry()
        #Somewhere around here I realized i should have just done it with js.
        if platform == 'facebook':
            new_entry['link'].label.text = 'Facebook Link'
            new_entry['link'].data = request.form.get('facebook','')
            new_entry['link'].name = 'facebook'
            new_entry['remove'].name = 'remove_facebook'
        elif platform == 'twitter':
            new_entry['link'].label.text = 'Twitter Link'
            new_entry['link'].name = 'twitter'
            new_entry['link'].data = request.form.get('twitter','')
            new_entry['remove'].name = 'remove_twitter'
        elif platform == 'instagram':
            new_entry['link'].label.text = 'Instagram Link'
            new_entry['link'].name = 'instagram'
            new_entry['link'].data = request.form.get('instagram','')
            new_entry['remove'].name = 'remove_instagram'
    #Save updated entries in session
    session['social_link_entries'] = saved_entries
    session.modified = True


@bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart=session.get('cart',None)
    form = CardDetails()
    db = get_db()
    tickets = []
    if cart is not None:
        ticket_ids = list(cart.keys())
    if cart is not None:
        tickets = Ticket.fetch_tickets_by_ids(db=db,ids=ticket_ids)
    sum = int_to_decimal(sum_prices_of_tickets(tickets))
    #NOTE: On form validate tickets are bought.
    if form.validate_on_submit():
        ownership = [Ownership(user_id=g.user,ticket_id=t_id) for t_id in ticket_ids]
        history = [History(user_id=g.user,action=ActionType.BUY_TICKET,ticket_id=t_id,id=uuid.uuid4()) for t_id in ticket_ids]
        seller_history = [History(user_id=t.seller_id,action=ActionType.SELL_TICKET,ticket_id=t.id,id=uuid.uuid4()) for t in tickets]
        for h in history:
            h.insert_entry(db)
        for o in ownership:
            o.insert_ownership_instance(db)
        for t in tickets:
            t.change_ticket_status(db)
        for sh in seller_history:
            sh.insert_entry(db)
        db.commit()
        cart.clear()
        session.modified = True
        close_db()
        return redirect(url_for("user.success"))
    close_db()
    return render_with_user('user/cart.html',tickets=tickets,sum=sum,form=form)
@bp.route('/success', methods=['GET', 'POST'])
@login_required
def success():
        return render_with_user('user/success.html')
@bp.route('/add-to-cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    id = request.args['id']
    cart = session.get('cart',{})
    cart[id] = True
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('user.cart'))
@bp.route('/remove-from-cart', methods=['GET', 'POST'])
@login_required
def remove_from_cart():
    id = request.args['id']
    cart = session.get('cart',{})
    if len(cart) != 0:
        del cart[id]
    session.modified = True
    return redirect(url_for('user.cart'))

@bp.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    #we don't need to pass a tickets object since it is contained in the user object which is implicitly passed
    #via the render_with_user function.
    return render_with_user('user/tickets.html')
