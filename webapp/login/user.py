from flask import Blueprint, redirect, url_for, request, session
from flask_login import logout_user

from webapp import google, facebook, login_manager
from webapp.login.models import User
from webapp.login.populate import auth_user

user_login = Blueprint("login", __name__)


@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(email=id).first()
    return user


@user_login.route('/login/<string:api>')
def login(api):
    if api == 'google':
        return google.authorize(callback=url_for('login.google_authorized', _external=True))
    else:
        callback = url_for(
            'login.facebook_authorized', next=request.args.get('next')
                                              or request.referrer
                                              or None,
            _external=True
        )
        return facebook.authorize(callback=callback)


@user_login.route("/logout")
def logout():
    session.pop('facebook_token', None)
    session.pop('google_token', None)
    session.permanent = False
    logout_user()

    return redirect(url_for('index'))


@user_login.route('/login/google_authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return auth_user(me.data, 'google')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@user_login.route('/login/facebook_authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me/?fields=email,name,id')
    return auth_user(me.data, 'facebook')


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')
