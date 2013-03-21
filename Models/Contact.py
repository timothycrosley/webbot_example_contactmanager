"""
    This is an example app engine data store model
    Modify freely to fit your purposes.
"""

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import search
from google.appengine.api import files

class Contact(search.SearchableModel):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    phone = db.StringProperty(required=False)
    last_updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)
