'''
    Defines how to store contacts
'''

from google.appengine.ext import db
from google.appengine.ext import search

class Contact(search.SearchableModel):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    phone = db.StringProperty(required=False)
    last_updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)
