import json

from flask.ext.api import status
import flask as fk

from newsdb.common import crossdomain
from news import app, SERVICE_URL, service_response
from newsdb.common.models import Radio

import mimetypes
import json
import traceback
import datetime
import random
import string
from io import StringIO
import hashlib

@app.route(SERVICE_URL + '/radio/add', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def add_radio():
    if fk.request.method == 'POST':
        if fk.request.data:
            data = json.loads(fk.request.data)
            name = data.get('name', None)
            country = data.get('country', None)
            url = data.get('url', '')
            language = data.get('language', None)
            if name is None or country is None or language is None:
                return service_response(405, 'Radio addition denied', 'A radio has to contain a name, country and language.')
            else:
                _radio = Radio.objects(name=name, country=country, language=language).first()
                if _radio is None:
                    _radio = Radio(created_at=str(datetime.datetime.utcnow()))
                    _radio.name = name
                    _radio.country = country
                    _radio.url = url
                    _radio.language = language
                    _radio.save()
                    return service_response(200, 'Radio created', 'The new radio was added')
                else:
                    return service_response(204, 'Radio addition denied', 'A radio with this name, country and language already exists.')
        else:
            return service_response(204, 'Radio addition failed', 'No data submitted.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

@app.route(SERVICE_URL + '/radio/edit/<radio_id>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def edit_radio(radio_id):
    if fk.request.method == 'GET':
        _radio = Radio.objects.with_id(radio_id)
        if _radio:
            if fk.request.data:
                data = json.loads(fk.request.data)
                name = data.get('name', _radio.name)
                country = data.get('country', _radio.country)
                url = data.get('url', _radio.url)
                language = data.get('language', _radio.language)

                _radio_check = Radio.objects(name=name, country=country, language=language).first()
                if _radio_check is None:
                    _radio.name = name
                    _radio.country = country
                    _radio.url = url
                    _radio.language = language
                    _radio.save()
                    return service_response(200, 'Edition succeeded', 'Radio {0} edited.'.format(radio_id))
                else:
                    return service_response(204, 'Radio edition denied', 'A radio with this name, country and language already exists.')
            else:
                return service_response(204, 'Radio addition failed', 'No data submitted.')
        else:
            return service_response(204, 'Unknown radio', 'No corresponding radio found.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(SERVICE_URL + '/radios/country/<country>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def radios_by_country(country):
    if fk.request.method == 'GET':
        if country == 'all':
            radios = [r.info() for r in Radio.objects()]
        else:
            radios = [r.info() for r in Radio.objects(country=country)]
        return service_response(200, 'Country {0} radios'.format(country), {'size':len(radios), 'radios':radios})
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(SERVICE_URL + '/radio/delete/<radio_id>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def delete_radio(radio_id):
    if fk.request.method == 'GET':
        _radio = Radio.objects.with_id(radio_id)
        if _radio:
            _radio.delete()
            return service_response(200, 'Deletion succeeded', 'Radio {0} deleted.'.format(radio_id))
        else:
            return service_response(204, 'Unknown radio', 'No corresponding radio found.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
