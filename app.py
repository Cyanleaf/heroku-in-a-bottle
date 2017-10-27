#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
import json
import urllib.request
import bleach
from sys import argv
api = {'car': 'http://apis.is/car?number={}', 'company': 'http://apis.is/company?{}={}'}
links = {'car': 'Car', 'company': 'Company'}


def get_api_data(api_):
    with urllib.request.urlopen(api_) as dump:
        data = json.loads(dump.read().decode())
    return data


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
    if len(list(bottle.request.forms)) > 0:
        try:
            item = [bleach.clean(bottle.request.forms.get(b)) for b in [x for x in bottle.request.forms]]
            print(item)
            if len(item) == 1:
                info = get_api_data(api[id].format(item[0]))
                info.update({'multi': True, 'id': id})
            else:
                info = get_api_data(api[id].format(item[1], item[0]))
                print(info['results'][0])
                info.update({'multi': True, 'id': id})
            return bottle.template('{}_p.html'.format(id), info)
        except:
            print('EXCEPT:--')
            return bottle.template('error.html', {'multi': True, 'id': id})

    else:
        info = get_api_data(api[id])
        info['results']['multi'] = False
        return bottle.template('', info)


@bottle.get('/s/<path:re:.*\.(png|jpg|json|css)>')
def static(path):
    return bottle.static_file(path, root='./st')

bottle.run(host='localhost', port=80, reloader=False)
