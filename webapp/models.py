from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from webapp.app import db

#####################################################################
#  Create tables: category and item
#
#  category is to store sport category
#  item is to store all items corresponding to category
#  item has a foreign key pointing to category
#####################################################################

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    item = relationship("Item", backref="Category")


class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(255), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(String(255))
    cat_id = Column(Integer, ForeignKey('category.id'), nullable=False)
