from flask import (
    Blueprint,url_for,g,session,request,redirect
)
import uuid
from copy import deepcopy
from ..forms.user import UpdateUserForm,SocialForm
from ..forms.auth import SignUpForm
from ..models.user import User
from ..models.history import History,ActionType
from ..utils import render_with_user
from ..database import get_db,close_db
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    history = None
    if g.user is not None:
        db = get_db()
        history = History.fetch_history(db,g.user)
        close_db()
    return render_with_user('user/profile.html',history=history)
@bp.route('/history', methods=['GET', 'POST'])
def history():
    return render_with_user('user/profile.html')
@bp.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateUserForm()
    form.process(request.form)
 
    #session['social_link_entries'] = {}
    saved_entries = session.get('social_link_entries', {})
    if form.is_submitted():
        if form.social_media_platform.add.data == True:  
                platform = form.social_media_platform.data['social_media_platform']
                saved_entries[platform]= ''
                populate_platforms(saved_entries=saved_entries,form=form)
        elif form.save.data == True:
            if form.validate():
                db = get_db()
                user = User.from_db(db,g.user).update_from_form(form,request,db)
                history = History(id=uuid.uuid4(),user_id=g.user,action=ActionType.UPDATED_PROFILE)
                print(str(history.id))
                #be4bc646-28e5-4efe-887f-c50da2e48066
                history.insert_entry(db)
                db.commit()
                close_db()
                del saved_entries
                session.modified=True
                return redirect(url_for('user.profile'))
            populate_platforms(saved_entries=saved_entries,form=form)   
            return render_with_user('user/update.html',form=form)
        else:
            relevant_fields = {}
            for key, value in request.form.items():
                if key.startswith(('facebook', 'twitter', 'instagram', 'remove_')):
                    relevant_fields[key] = value
            remove_social_media = None
            for key, value in relevant_fields.items():
                if key.startswith("remove_") and value == "Remove":
                    remove_social_media = key[len("remove_"):]
                    if remove_social_media in saved_entries:
                        saved_entries.pop(remove_social_media)
                    populate_platforms(saved_entries=saved_entries,form=form)
    
    populate_platforms(saved_entries,form)
    return render_with_user('user/update.html',form=form)


def populate_platforms(saved_entries,form):
    print(len(form.social_link))
    while form.social_link.entries:
        form.social_link.pop_entry()
    for platform in saved_entries:
        new_entry = form.social_link.append_entry()
        if platform == 'facebook':
            print(request.form)
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
    # Save the updated entries in the session
    session['social_link_entries'] = saved_entries
    session.modified = True