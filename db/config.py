import os


# calculate location of default sqlite db file so it
# can be referenced from both top level directory 
# by project.py and files in db/ directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
default_sqlite_uri = 'sqlite:///' +  os.path.join(BASE_DIR, 'catalog.db')

initial_category_names = [
     'Soccer', 'Basketball', 'Baseball', 'Frisbee',
     'Snowboarding','Rock Climbing', 'Foosball',
     'Skating', 'Hockey']

number_of_latest_items = 10
