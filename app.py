#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
import requests
import bleach
from sys import argv
api = {'car': 'http://apis.is/car?{}={}', 'company': 'http://apis.is/company?{}={}'}
links = {'car': 'Car', 'company': 'Company'}
headers = {'accept-version': '1', 'user-agent': 'Kristjaninfo/0.0.1'}


def get_api_data(api_):
    data = requests.get(api_, headers=headers)
    return data.json()


@bottle.error(404)
def error404(error):
    return bottle.template('error.html')


@bottle.route('/')
def index():
    return bottle.template('inde.html')


@bottle.route('/404')
def rais_404():
    raise bottle.HTTPError(404)


@bottle.get('/<id>')
def get_api(id):
    try:
        return bottle.template('{}.html'.format(id), {'multi': False})
    except:
        raise bottle.HTTPError(404)


@bottle.post('/<id>')
def post_api(id):
    try:
        name = bleach.clean(bottle.request.forms.name)
        titi = bleach.clean(bottle.request.forms.titi)
        print(name, titi)
        info = get_api_data(api[id].format(titi, name))
        print(get_api_data(api[id].format(titi, name)))
        info.update({'multi': True, 'id': id})
        print(info['results'][0])
        return bottle.template('{}_p.html'.format(id), info)
    except:
        print('EXCEPT:--')
        return bottle.template('error.html', {'multi': True, 'id': id})


@bottle.get('/s/<path:re:.*\.(png|jpg|json|css)>')
def static(path):
    return bottle.static_file(path, root='./st')

bottle.run(host='0.0.0.0', port=argv[1], reloader=False)
