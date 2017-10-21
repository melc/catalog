from datetime import timedelta
from flask import request, render_template, flash, g, session, jsonify
from flask_login import login_required, current_user

from webapp.app import app
from webapp.forms import AddItem, EditItem, DeleteItem, AddCat, EditCat, flash_errors

from webapp.populate import insert_cat, update_cat, insert_item, update_item, delete_item, \
    get_category, get_latest_items, get_item_by_cat, get_cat_for_item, get_all_items


@app.before_first_request
def initialize_user():
    session.permanent = True  # set permanent_session
    app.permanent_session_lifetime = timedelta(days=7)  # set permanent_session valid for 7 days

    if current_user.is_authenticated:
        g.user = current_user
    else:
        g.user = None


@app.route('/', methods=['GET'])
def index():
    # Main page of Catalog App                                     #
    # boolHome is a passing parameter to indicate the              #
    # render template is either a home page or editable page       #
    return render_template('index.html',
                           catLists=get_category(), lateLists=get_latest_items(), boolHome='True')


@app.route('/category/<string:name>/Items')
def category(name):
    # Render template to display all items corresponding to the selected category
    return render_template('index.html', catLists=get_category(),
                           countCats=get_cat_for_item(name),
                           catItems=get_item_by_cat(name), boolHome='False', model='None')


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_cat():
    # Render template to display all categories after creating a new category   #
    # modal is a passing parameter to either keep bootstrap modal open for      #
    # handling error events or render template for successful add/edit/delete   #
    form = AddCat(request.form)
    if request.method == 'POST' and form.validate():

        if insert_cat(form.name.data):
            return render_template('index.html', catLists=get_category(), boolHome='True', modal='None')
        else:
            flash('Failed to create a new category. Try Again!', 'error')
    else:
        flash_errors(form)

    return render_template('index.html', catLists=get_category(), lateLists=get_latest_items(), boolHome='True', form=form, modal='add-cat')


@app.route('/category/edit', methods=['GET', 'POST'])
@login_required
def edit_cat():
    # render template to display all categories after updating an existing category
    form = EditCat(request.form)
    if request.method == 'POST' and form.validate():
        dict = {}
        dict["id"] = form.id.data
        dict["name"] = form.name.data

        if update_cat(dict):
            return render_template('index.html', catLists=get_category(), countCats=get_cat_for_item(form.name.data),
                           catItems=get_item_by_cat(form.name.data), boolHome='False', modal='None')
        else:
            flash('Failed to update this category. Try Again!', 'error')
    else:
        flash_errors(form)

    return render_template('index.html', catLists=get_category(), lateLists=get_latest_items(), boolHome='True', form=form,
                           modal='edit-cat-' + str(form.id.data))


@app.route('/category/<string:name>/add', methods=['GET', 'POST'])
@login_required
def add_item(name):
    # render template to display all items after creating a new item for the selected category
    form = AddItem(request.form)
    if request.method == 'POST' and form.validate():
        dict = {}
        dict["title"] = form.title.data
        dict["desc"] = form.desc.data
        dict["cat_id"] = form.cat_id.data
        dict["user"] = "admin"

        if insert_item(dict):

            return render_template('index.html', catLists=(get_category()),
                                   countCats=get_cat_for_item(name),
                                   catItems=get_item_by_cat(name), boolHome='False', modal='None')
        else:
            flash('Failed to create a new item. Try Again!', 'error')
    else:
        flash_errors(form)

    return render_template('index.html', catLists=get_category(), boolHome='True', form=form,
                           modal='add-item-' + str(form.cat_id.data))


@app.route('/category/<string:title>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(title):
    # render template to display all items after updating an existing item corresponding to a selected category
    form = EditItem(request.form)
    if request.method == 'POST' and form.validate():
        dict = {}
        dict["name"] = form.name.data
        dict["title"] = form.title.data
        dict["desc"] = form.desc.data
        dict["item_id"] = form.item_id.data
        dict["updated_by"] = 'admin'

        if update_item(dict):

            return render_template('index.html', catLists=get_category(),
                                   countCats=get_cat_for_item(form.name.data), catItems=get_item_by_cat(form.name.data),
                                   boolHome='False', modal='None')
        else:
            flash('Failed to update the item. Try Again!', 'error')
    else:
        flash_errors(form)

    return render_template('index.html', catLists=get_category(), boolHome='True', form=form,
                           modal='edit-item-' + str(form.item_id.data))


@app.route('/category/<string:title>/delete', methods=['GET', 'POST'])
@login_required
def del_item(title):
    # render template to display all items after deleting an item corresponding to a selected category
    form = DeleteItem(request.form)
    if request.method == 'POST' and form.validate():

        if delete_item(form.item_id.data):

            return render_template('index.html', catLists=get_category(),
                                   countCats=get_cat_for_item(form.name.data), catItems=get_item_by_cat(form.name.data),
                                   boolHome='False', modal='None')
        else:
            flash('Failed to delete the item. Try Again!', 'error')

    else:
        flash_errors(form)

    return render_template('index.html', catLists=get_category(), boolHome='True', form=form,
                           modal='delete-item-' + str(form.item_id.data))


@app.route('/catalog.json')
def json_map():
    # print json format of catalog dataset
    return jsonify(get_all_items())
