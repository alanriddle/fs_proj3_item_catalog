from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User
from config import default_sqlite_uri, initial_category_names
from config import number_of_latest_items
              

def db_create_session(sqlite_db_uri=default_sqlite_uri):
    engine = create_engine(sqlite_db_uri)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def db_add_categories(session, category_names):
    """Add specified category_names to database."""
    for category_name in category_names:
        category = Category(name=category_name)
        session.add(category)
        session.commit()    # if a lot, consider batching in a transaction


def db_add_item_using_category_name(session, category_name, item_name, item_description, user_id):
    """Add an item to database with specified category_name.

    Example:
        To add a 'soccer ball' item:
            db_add_item_using_category_name(session, 'Soccer', 'Soccer ball',
                                            'Fast, light official soccer ball.', login_session['id'])
            (where 'Soccer' is a preexisting category name.)
    """
    category = session.query(Category).filter_by(name=category_name).one()
    new_item = Item(name=item_name,
                       description=item_description,
                       category_id=category.id)
    session.add(new_item)
    session.commit()


def db_categories(db_session):
    """List of all categories in database sorted alphabetically."""
    categories = db_session.query(Category).order_by(Category.name).all()
    print 'db_categories: ...'
    print 'len(categories) = ' + str(len(categories))
    return categories


def db_category(db_session, category_id):
    """Category with specified id."""
    category = db_session.query(Category).filter_by(id=category_id).one()
    return category


def db_items_in_category(db_session, category_id):
    """List of items which have specified category id."""
    items = db_session.query(Item).filter_by(category_id=category_id).order_by(Item.name).all()
    return items


def db_item(db_session, item_id):
    """Item with specified id."""
    item = db_session.query(Item).filter_by(id=item_id).one()
    return item


def db_latest_items(db_session, number_of_items=number_of_latest_items):
    """Return most recent items added to database."""
    latest_items = db_session.query(Item).order_by(Item.created.desc()).limit(number_of_items)
    return latest_items


def db_save_item(session, item):
    """Save item in database."""
    session.add(item)
    session.commit()

def db_delete_item(session, item):
    """Delete item in database."""
    session.delete(item)
    session.commit()


def db_update_user(db_session, login_session):
    # if user is not already in db:
    #     insert into db
    user_id = login_session['id']
    user = db_session.query(User).filter_by(id=user_id).all()
    if not user:
        user = User()
        user.id = user_id
        db_session.add(user)
        db_session.commit()
