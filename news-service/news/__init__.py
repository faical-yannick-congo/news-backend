"""CoRR api module."""
import flask as fk
from newsdb.common.core import setup_app
from newsdb.common.models import Radio
from newsdb.common.models import Coverage
from newsdb.common.models import News
import tempfile
from io import StringIO
from io import BytesIO
import os
import simplejson as json
import datetime
import traceback

import requests
from datetime import date, timedelta
from functools import update_wrapper
from calendar import monthrange
import time

import glob

# Flask app instance
app = setup_app(__name__)

# The sms news service's version
SERVICE_VERSION = 0.1
# The sms news service base url
SERVICE_URL = '/sms/services/news/v{0}'.format(SERVICE_VERSION)


def service_response(code, title, content):
    """Provides a common structure to represent the response
    from any api's endpoints.
        Returns:
            Flask response with a prettified json content.
    """
    import flask as fk
    response = {'service':'sms-news', 'code':code, 'title':title, 'content':content}
    return fk.Response(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')), mimetype='application/json')

def data_pop(data=None, element=''):
    """Pop an element of a dictionary.
    """
    if data != None:
        try:
            del data[element]
        except:
            pass

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def smartWelcome(country=None):
    if country in ["212"]:
        return "Bienvenue dans le service de messagerie. Nous vous remercions de nous avoir fait confiance dans la prestation de vos nouvelles quotidiennes."
    elif country in ["34"]:
        return "Bienvenido al servicio de mensajeria. Gracias por confiar en nosotros en la entrega de sus noticias diarias."
    elif country in ["33", "226", "227"]:
        return "Bienvenue dans le service de messagerie. Nous vous remercions de nous avoir fait confiance dans la prestation de vos nouvelles quotidiennes."
    else:
        return "Welcome to the News Messaging Service. Thank you for trusting us in delivering your daily news."

def news_importance(message):
    bag_of_words = ["important", "alert", "mort", "dead", "death", "kill", "tue", "catastroph", "perte", "explosion", "terror", "bomb", "crash", "accident"]
    bag_of_words.append("incendie")
    bag_of_words.append("feu")
    bag_of_words.append("fire")
    bag_of_words.append("police")
    bag_of_words.append("attaque")
    bag_of_words.append("attack")
    bag_of_words.append("assassin")
    bag_of_words.append("poison")
    bag_of_words.append("guerr")
    bag_of_words.append("war")
    bag_of_words.append("humanit")
    bag_of_words.append("kidnap")
    bag_of_words.append("violen")
    bag_of_words.append("gun")
    bag_of_words.append("arme")
    bag_of_words.append("fire")
    words = message.split(" ")
    indice = len(words)
    for word in words:
        if word in bag_of_words:
            indice = indice + 10
    return indice



# import all the api endpoints.
import news.endpoints
