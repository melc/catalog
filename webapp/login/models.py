from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from webapp.models import db


#####################################################################
#  Create table: users
#  users is to store user information for accessing catalog app
#####################################################################

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255))
    fullname = Column(String(255))
    avatar = Column(String(255))
    api_name = Column(String(20))
    api_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(255), nullable=False)

    @property
    def is_active(self):
        """True, as all users are active."""
        return True

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email
