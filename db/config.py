"""
This file contains the following configurable variables:
    - default_sqlite_url - catalog.db
    - initial_category_names - list of sporting goods categories
    - number_of_latest_items - how many of the latest items to display
                               on the main catalog page
"""

import os


# calculate location of default sqlite db file so it
# can be referenced from both top level directory 
# by project.py and files in db/ directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
default_sqlite_uri = 'sqlite:///' +  os.path.join(BASE_DIR, 'catalog.db')

# add support for Postgresql database
sqlalchemy_database_uri = "postgresql://catalog:catalog_super_secret@localhost/catalog"

default_database_uri = sqlalchemy_database_uri

initial_category_names = [
     'Soccer', 'Basketball', 'Baseball', 'Frisbee',
     'Snowboarding','Rock Climbing', 'Foosball',
     'Skating', 'Hockey']

number_of_latest_items = 10
