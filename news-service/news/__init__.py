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

def news_importance(message=None):
    bag_of_words = ["important", "alert", "mort", "dead", "death", "kill", "tue", "catastroph", "perte", "explosion"]
    bag_of_words.extend(["incendie", "feu", "fire", "police", "attaque", "attack", "assassin", "poison", "guerr", "war"])
    bag_of_words.extend(["humanit", "kidnap", "violen", "gun", "arme", "fire", "election", "prison", "save", "sauve"])
    bag_of_words.extend(["bad", "mauvais", "good", "bon", "ban", "interdi", "help", "aide", "vol", "steel", "rub", "terror"])
    bag_of_words.extend(["hirt", "bless", "beauti", "rare", "child", "wom", "black", "white", "epic", "virus", "bacter"])
    bag_of_words.extend(["exception", "vaccin", "deas", "malad", "viral", "vital", "critical", "fatal", "happ", "heure"])
    bag_of_words.extend(["hot", "negocia", "paix", "peace", "united", "reconci", "nuclear", "bomb", "crash", "accident"])
    bag_of_words.extend(["tens", "tendu", "abduct", "viol", "rape", "freedom", "liber", "jail", "banqu", "bank", "welcome"])

    if message:
        words = message.split(" ")
        indice = len(words)
        for word in words:
            if word.lower() in bag_of_words:
                indice = indice + 5
        return indice
    else:
        return 0

def get_one_number(country):
    r = requests.get('http://54.196.141.56:5300/sms/services/sso/v0.1/users/country/{0}'.format(country))
    response = json.loads(r.text)
    return response['content']['users'][0]['phone']


# import all the api endpoints.
import news.endpoints
