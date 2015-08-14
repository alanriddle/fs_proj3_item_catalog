from flask import (Flask, render_template, request, redirect,
                   make_response, url_for, flash, jsonify)
app = Flask(__name__)

from db.database_setup import Category, Item, User
from db.database_access import db_create_session, db_categories, db_category
from db.database_access import db_items_in_category, db_item, db_save_item
from db.database_access import db_delete_item, db_latest_items

from util import item_from_request_post, make_response
from login import(upgrade_to_credentials, token_info, is_already_logged_in, 
                  get_user_info, update_login_session)


session = db_create_session()

is_logged_in = True

########## Routes for home page
@app.route('/')
@app.route('/index/')
@app.route('/catalog/')
def catalog():
    categories = db_categories(session)
    latest_items = db_latest_items(session)
    return render_template('catalog.html', categories=categories, latest_items=latest_items, is_logged_in=is_logged_in)


@app.route('/catalog/json/')
def catalog_as_json():
    return 'routed by /catalog.json/'


########## Routes for items in specified category
@app.route('/catalog/category/<int:category_id>/')
def show_items_in_category(category_id):
    category = db_category(session, category_id)
    items = db_items_in_category(session, category_id)
    return render_template('category.html', category=category, items=items, is_logged_in=is_logged_in)


@app.route('/catalog/category/<int:category_id>/json/')
def items_in_category_as_json(category_id):
    return 'routed by /catalog/category/' + str(category_id) + '/json/'


########## Routes for specified category and item
@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/')
def show_item(category_id, item_id):
    category = db_category(session, category_id)
    item = db_item(session, item_id)
    return render_template('item.html', category=category, item=item,
                           is_logged_in=is_logged_in,  is_logged_in_owner=is_logged_in)



@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/json/')
def item_as_json(category_id, item_id):
    return 'routed by /catalog/category/' + str(category_id) + '/item/' + str(item_id) + '/json/'


########## Routes for add item to category 
@app.route('/catalog/category/<int:category_id>/item/add/', methods=['GET', 'POST'])
def add_item(category_id):
    if request.method == 'POST':
        item = item_from_request_post(request)
        if item:
            item.category_id = category_id
            db_save_item(session, item)
            return redirect(url_for('show_items_in_category', category_id=category_id))
        else:
            # problem with item, try again
            return redirect(url_for('add_item', category_id=category_id))
    else:
        category = db_category(session, category_id)
        return render_template('additem.html', category=category)


########## Route to edit item in category
@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    if request.method == 'POST':
        item_from_database = db_item(session, item_id)
        item_from_form = item_from_request_post(request)
        if item_from_form:
            item_from_database.name = item_from_form.name
            item_from_database.description = item_from_form.description

            session.commit()
            return redirect(url_for('show_items_in_category', category_id=category_id))
        else:
            # problem with item, try again
            return redirect(url_for('edit_item', category_id=category_id, item_id=item_id))
    else:
        category = db_category(session, category_id)
        item = db_item(session, item_id)
        cancel_url = '/catalog/category/' + str(item.category_id) + '/item/' + str(item_id)
        return render_template('edititem.html', category=category, item=item, cancel_url=cancel_url, is_logged_in=is_logged_in)


########## Route to delete item in category
@app.route('/catalog/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    if request.method == 'POST':
        item = db_item(session, item_id)
        if item:
            db_delete_item(session, item)
            return redirect(url_for('show_items_in_category', category_id=category_id))
        else:
            # problem with item, try again
            return redirect(url_for('delete_item', category_id=category_id, item_id=item_id))
    else:
        category = db_category(session, category_id)
        item = db_item(session, item_id)
        return render_template('deleteitem.html', category=category, item=item)


########### login 
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        return json_response('Invalid state parameter', 400)

    authorization_code = request.data

    try:
        credentials = upgrade_to_credentials(authorization_code)
    except FlowExchangeError:
        return json_response('Failed to upgrade the authorization code.', 401)

    access_token_info = token_info(access_token)
    if access_token_info.get('error') is not None:
        error = access_token_info.get('error')
        return json_response(error, 500)

    gplus_id = credentials.id_token['sub']
    if access_token_info['user_id'] != gplus_id:
        return json_response("Token's user ID doesn't match given user ID.", 401)

    if access_token_info['issued_to'] != CLIENT_ID:
        return json_response("Token's client ID does not match this app.", 401)

    if is_already_logged_in():
        return json_response("Current user is already connected.", 401)

    user_info = get_user_info(credentials.access_token)
    update_login_session(credentials, gplus_id, user_info)

    flash("You are now logged in as %s" % login_session['username'])
    return render_template('gconnect.html', login_session=login_session)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

