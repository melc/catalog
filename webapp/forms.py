from wtforms import StringField, TextAreaField, IntegerField, validators, Form
from flask import flash

# set error messages of form validation
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error: %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

# validate form elements of creating category
class AddCat(Form):
    name = StringField("name", [validators.InputRequired()])


# validate form elements of updating category
class EditCat(Form):
    name = StringField('name', [validators.InputRequired()])
    id = IntegerField('id')


# validate form elements of creating item
class AddItem(Form):
    title = StringField('title', [validators.InputRequired()])
    desc = TextAreaField("desc")
    cat_id = IntegerField('cat_id')


# validate form elements of updating item
class EditItem(Form):
    name = StringField('name')
    title = StringField('title', [validators.InputRequired()])
    desc = TextAreaField("desc")
    cat_id = IntegerField('cat_id')
    item_id = IntegerField("item_id")


# validate form elements of deleting item
class DeleteItem(Form):
    name = StringField('name')
    item_id = IntegerField('item_id')
    title = StringField('title')
