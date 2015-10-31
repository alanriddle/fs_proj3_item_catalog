"""
This file loads the initial category names into the database.

It is run from the command line.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base
from database_access import db_create_session, db_add_categories

from config import initial_category_names


db_session = db_create_session()
db_add_categories(db_session, initial_category_names)

