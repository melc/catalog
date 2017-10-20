from sqlalchemy.sql import exists, text, func
from webapp.app import db
from webapp.models import Item, Category
from flask import flash


#######################################################
# SELECT statements
#######################################################

# return all categories
def get_category():
    list = []
    for row in Category.query.order_by(Category.id).all():
        (row.__dict__).pop('_sa_instance_state', None)
        list.append(row.__dict__)

    return list


# return all items and categories to print catalog.json endpoint
def get_all_items():
    dict = {}
    list = []

    # convert category query result to dictionary
    for row_cat in Category.query.order_by(Category.id).all():

        (row_cat.__dict__).pop('_sa_instance_state', None)
        dict_cat = row_cat.__dict__
        catid = (row_cat.__dict__)["id"]

        list_cat = []

        # convert item query result to dictionary and
        # store all items corresponding to a category
        # in array
        for row_item in Item.query.filter(Item.cat_id == catid).all():
            (row_item.__dict__).pop('_sa_instance_state', None)

            list_cat.append(row_item.__dict__)

        dict_cat["Item"] = list_cat
        list.append(dict_cat)

    dict["Category"] = list

    return dict


# return 20 most recent items
def get_latest_items():
    return Item.query.order_by(Item.created_at.desc()).limit(20).all()


# return all items by selected category
def get_item_by_cat(cat_name):
    list = []
    for row in Item.query.join(Category).filter(Item.cat_id == Category.id). \
            filter(func.lower(Category.name) == func.lower(cat_name)).order_by(Item.title).all():
        (row.__dict__).pop('_sa_instance_state', None)
        list.append(row.__dict__)

    return list


# return number of items corresponding to selected category
def get_cat_for_item(name):
    sqlstat = \
        "SELECT name, cnt, id FROM category, " \
        "( " \
        "SELECT name AS c_name, COALESCE(cnt, 0) AS cnt FROM CATEGORY " \
        "LEFT JOIN( " \
        "SELECT cat_id, COUNT(cat_id) AS cnt FROM CATEGORY " \
        "LEFT JOIN item ON CATEGORY.id = item.cat_id " \
        "GROUP BY cat_id) AS count_item ON id = cat_id) AS coalesce_item WHERE " \
        "name = c_name AND lower(name) = '" + name.lower() + "'"

    result = db.engine.execute(text(sqlstat))
    for row in result:
        ret = dict(row)

    result.close()

    return ret


#########################################
# INSERT, UPDATE category
#########################################

# add category
def insert_cat(name):
    (ret,), = db.session.query(exists().where(Category.name.ilike(name)))

    if ret:
        flash(name + " category already existed.", 'error')
        return False

    else:
        try:
            new_cat = Category(
                name=name,
            )
            db.session.add(new_cat)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()


# update category
def update_cat(itemlist):
    (ret,), = db.session.query(exists().where(Category.name.ilike(itemlist["name"])))

    if ret:
        flash(itemlist["name"] + " category already existed.", 'error')
        return False
    else:

        try:
            db.session.query(Category).filter_by(id=itemlist["id"]).update({"name": itemlist["name"]})
            db.session.commit()
            return True
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()


#############################################
# INSERT, UPDATE, and DELETE item
#############################################

# create a new item
def insert_item(itemlist):
    try:
        new_item = Item(
            title=itemlist["title"],
            description=itemlist["desc"],
            created_by=itemlist["user"],
            cat_id=itemlist["cat_id"],
        )
        db.session.add(new_item)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


# update item contents
def update_item(itemlist):
    try:
        qry, = db.session.query(Category.id).filter(func.lower(Category.name) == func.lower(itemlist["name"])).one()
        db.session.query(Item).filter_by(id=itemlist['item_id']).update({"title": itemlist['title'],
                                                                         "description": itemlist["desc"],
                                                                         "updated_by": itemlist["updated_by"],
                                                                         "cat_id": qry})
        db.session.commit()
        return True
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()


# delete an item
def delete_item(item_id):
    try:
        db.session.query(Item).filter_by(id=item_id).delete()
        db.session.commit()
        return True
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
