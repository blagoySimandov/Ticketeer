from flask import (
    Blueprint,url_for,g,session,request,redirect
)
import uuid
from ..forms.user import UpdateUserForm
from ..models.user import User
from .auth import login_required
from ..views.post import save_file
from ..models.history import History,ActionType
from ..utils import render_with_user,save_file
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
@login_required
@bp.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateUserForm()
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
                user = User.from_db(db,g.user)
                if form.profile_picture.data is not None:
                    f = form.profile_picture.data
                    print('file')
                    hashed_f_name = uuid.uuid4()
                    save_file(f,'static/profile_pics',hashed_f_name,)
                    user.profile_picture = hashed_f_name
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
    #Save updated entries in session
    session['social_link_entries'] = saved_entries
    session.modified = True