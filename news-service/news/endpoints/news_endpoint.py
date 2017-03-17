import json

from flask.ext.api import status
import flask as fk

from newsdb.common import crossdomain
from news import app, SERVICE_URL, service_response
from newsdb.common.models import Radio, Coverage, News

import mimetypes
import json
import traceback
import datetime
import random
import string
from io import StringIO
import hashlib

@app.route(SERVICE_URL + '/news/add', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def add_news():
    if fk.request.method == 'POST':
        if fk.request.data:
            data = json.loads(fk.request.data)
            radio = data.get('radio', None)
            coverage = data.get('coverage', None)
            content = data.get('content', None)
            _radio = Radio.objects.with_id(radio)
            _coverage = Coverage.objects.with_id(coverage)
            if _radio is None or _coverage is None or content is None:
                return service_response(405, 'News addition denied', 'A news has to contain a radio, a coverage and content.')
            else:
                _news = News.objects(radio=_radio, content=content, coverage=_coverage).first()
                if _news is None:
                    _news = News(created_at=str(datetime.datetime.utcnow()))
                    _news.radio = radio
                    _news.content = content
                    _news.country = country
                    _news.coverage = coverage
                    _news.save()
                    return service_response(200, 'News created', 'News added with success.')
                else:
                    return service_response(204, 'News addition denied', 'A News with this radio and content already exists.')
        else:
            return service_response(204, 'News addition failed', 'No data submitted.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a POST method.')

@app.route(SERVICE_URL + '/news/edit/<news_id>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def edit_news(news_id):
    if fk.request.method == 'GET':
        _news = News.objects.with_id(news_id)
        if _news:
            if fk.request.data:
                data = json.loads(fk.request.data)
                radio = data.get('radio', str(_news.radio.id))
                coverage = data.get('coverage', str(_news.coverage.id))
                content = data.get('content', _news.content)
                status = data.get('status', _news.status)
                received = data.get('received', _news.received)
                country = data.get('country', _news.country)

                _radio = Radio.objects.with_id(radio)
                _coverage = Coverage.objects.with_id(coverage)
                if _radio is None or _coverage is None or content is None:
                    return service_response(405, 'News edition denied', 'A news has to contain a radio, a coverage and content.')

                _news_check = News.objects(radio=radio, content=content, status=status).first()
                if _news_check is None:
                    _news.radio = radio
                    _news.content = content
                    _news.status = status
                    _news.received = received
                    _news.country = country
                    _news.save()
                    return service_response(200, 'Edition succeeded', 'News {0} edited.'.format(news_id))
                else:
                    return service_response(204, 'News edition denied', 'A news with this radio, content and status already exists.')
            else:
                return service_response(204, 'News edition failed', 'No data submitted.')
        else:
            return service_response(204, 'Unknown coverage', 'No corresponding coverage found.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

## pull news based on the coverage.
## Look for latest one with status to pushed
## Mark it to pulling and return it.
## Later on edit it to pulled when message done sent.

@app.route(SERVICE_URL + '/news/pushing/<country>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def news_pushing_country(country):
    if fk.request.method == 'GET':
        day = str(datetime.date.today().isoformat())

        news_pulled = News.objects(country=country, status='pulled', day=day).first()

        if news_pulled:
            news_pulled.satus = 'pushing'
            news_pulled.save()
            news_pushing = news_pulled.info()
            return service_response(200, 'News to send', news_pulled.info())
        else:
            return service_response(204, 'No news to send', "no news at this point.")
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(SERVICE_URL + '/news/pushed/<news_id>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def pushed_news(news_id):
    if fk.request.method == 'GET':
        _news = News.objects.with_id(news_id)
        if _news:
            _news.status = 'pushed'
            _news.save()
            return service_response(200, 'News pushed', 'News {0} was confimed pushed.'.format(news_id))
        else:
            return service_response(204, 'Unknown news', 'No corresponding news found.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(SERVICE_URL + '/news/country/<country>/<schedule>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def news_by_country(country, schedule):
    if fk.request.method == 'GET':

        if country == 'all':
            if schedule == 'all':
                news = [n.info() for n in News.objects()]
            else:
                news = [n.info() for n in News.objects(schedule=schedule)]
                for n in News.objects(status=schedule):
                    news.append(n.info())
        else:
            news = []
            if schedule == 'all':
                for n in News.objects(country=country):
                    news.append(n.info())
            else:
                for n in News.objects(country=country, schedule=schedule):
                    news.append(n.info())
                for n in News.objects(country=country, status=schedule):
                    news.append(n.info())
        return service_response(200, 'Country {0} News with Schedule {1}'.format(country, schedule), {'size':len(news), 'covers':news})
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(SERVICE_URL + '/news/today/<country>/<schedule>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def news_today_country(country, schedule):
    if fk.request.method == 'GET':
        day = str(datetime.date.today().isoformat())
        if country == 'all':
            if schedule == 'all':
                news = [n.info() for n in News.objects(day=day)]
            else:
                news = [n.info() for n in News.objects(day=day, schedule=schedule)]
                for n in News.objects(day=day, status=schedule):
                    news.append(n.info())
        else:
            news = []
            if schedule == 'all':
                for n in News.objects(country=country, day=day):
                    news.append(n.info())
            else:
                for n in News.objects(country=country, day=day, schedule=schedule):
                    news.append(n.info())
                for n in News.objects(country=country, day=day, status=schedule):
                    news.append(n.info())
        return service_response(200, 'Country {0} News with Schedule {1}'.format(country, schedule), {'size':len(news), 'news':news})
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')

@app.route(SERVICE_URL + '/news/delete/<country>/<news_id>', methods=['GET','POST','PUT','UPDATE','DELETE'])
@crossdomain(fk=fk, app=app, origin='*')
def delete_news(country, news_id):
    if fk.request.method == 'GET':
        for _new in News.objects():
            _new.delete()
        if news_id == "all":
            for _new in News.objects(country=country):
                _new.delete()
            return service_response(200, 'Deletion succeeded', 'All news deleted')
        else:
            _news = News.objects.with_id(news_id)
            if _news:
                _news.delete()
                return service_response(200, 'Deletion succeeded', 'News {0} deleted.'.format(news_id))
            else:
                return service_response(204, 'Unknown news', 'No corresponding news found.')
    else:
        return service_response(405, 'Method not allowed', 'This endpoint supports only a GET method.')
