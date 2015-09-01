"""
This file contains convenience/helper functions for project.py (that
are not specific to logging in or out - those helper functions 
found in login.py).

The intent of this file is to simplify code in project.py.
"""

import json
from flask import make_response

from db.database_setup import Item


def item_from_request_post(request):
    """Build Python object (item) from request."""
    if request.form['name']:
        item = Item()
        item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
            return item
    return None   # name and description required


def json_response(msg, code):
    response = make_response(json.dumps(msg), code)
    response.headers['Content-Type'] = 'application/json'
    return response



