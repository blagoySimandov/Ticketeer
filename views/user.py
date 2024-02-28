from flask import (
    Blueprint,url_for,g,session,request
)
from copy import deepcopy
from ..forms.user import UpdateUserForm,SocialForm
from ..forms.auth import SignUpForm
from ..models.history import History
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
    print(request.method)
    if form.is_submitted():
        if form.social_media_platform.add.data == True:  
                platform = form.social_media_platform.data['social_media_platform']
                saved_entries[platform]=True
                populate_platforms(saved_entries=saved_entries,form=form)
        elif form.save.data == True:      
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
                    print(form.social_link.data)
                    populate_platforms(saved_entries=saved_entries,form=form)
    return render_with_user('user/update.html',form=form)


def populate_platforms(saved_entries,form):
    print(len(form.social_link))
    while form.social_link.entries:
        form.social_link.pop_entry()
    for platform in saved_entries:
        new_entry = form.social_link.append_entry(form.social_link.data)
        if platform == 'facebook':
            new_entry['link'].label.text = 'Facebook Link'
            new_entry['link'].name = 'facebook'
            new_entry['remove'].name = 'remove_facebook'
        elif platform == 'twitter':
            new_entry['link'].label.text = 'Twitter Link'
            new_entry['link'].name = 'twitter'
            new_entry['remove'].name = 'remove_twitter'
        elif platform == 'instagram':
            new_entry['link'].label.text = 'Instagram Link'
            new_entry['link'].name = 'instagram'
            new_entry['remove'].name = 'remove_instagram'
    # Save the updated entries in the session
    session['social_link_entries'] = saved_entries
    session.modified = True

#   platforms = session.get("platforms",{})
#     if request.form.get('add',None) is not None:
#         platform = request.form.get('social_media_platform',None)
#         if platform is not None:
#             platforms[platform] = True
#             session.modified = True
#     remove = request.args.get('remove_social')
    
#     if remove is not None:
#         if platforms.get(remove,None) is not None:
#             session['platforms'].pop(remove)
#             session.modified = True
#             print(platforms)

#     form = UpdateUserForm(request.form)
#      #using dict instead of set as set is not json serializeable (cannot be put in session)
#     if social.validate_on_submit():
#         platform = social.social_media_platform.data
#         print("maika ti typa prosta")
#         platforms[platform] = True
#         session['platforms'][platform] = True
#         session.modified = True
#         print(len(platforms),'\n')
#     if form.validate_on_submit():
#         print(form.facebook.data)

