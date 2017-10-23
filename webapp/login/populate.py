from flask import flash, render_template
from sqlalchemy import exists
from flask_login import login_user

from webapp.login.models import User, db
from webapp.populate import get_category, get_latest_items


#########################################
# Create a new google account user
#########################################


def insert_google_user(data):
    (ret,), = db.session.query(exists().where(User.email == data["email"]))

    if ret:
        flash("Another Account is registered with this email.", 'error')
        return False
    else:
        try:
            new_user = User(
                email=data["email"],
                username=data["email"],
                fullname=data["name"],
                avatar=data["picture"],
                api_name='google',
                api_id=data["id"],
                created_by=data["name"]
            )
            db.session.add(new_user)
            db.session.commit()

            return new_user

        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()


#########################################
# Create a new facebook account user
#########################################
def insert_facebook_user(data):
    (ret,), = db.session.query(exists().where(User.email == data["email"]))

    if ret:
        flash("Another Account is registered with this email.", 'error')
        return False
    else:
        try:
            new_user = User(
                email=data["email"],
                username=data["email"],
                fullname=data["name"],
                api_name='facebook',
                api_id=data["id"],
                created_by=data["name"]
            )
            db.session.add(new_user)
            db.session.commit()

            return new_user

        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()


#################################################
#  Authorize catalog app user
#################################################

def auth_user(data, api_name):
    user_info = User.query.filter_by(email=data["email"]).first()
    if user_info is None:
        if api_name is 'google':
            user_info = insert_google_user(data)
        else:
            user_info = insert_facebook_user(data)

        flash('Logged in successfully.')

    login_user(user_info, remember=True)

    return render_template('index.html',
                           catLists=get_category(), lateLists=get_latest_items(), boolHome='True')
