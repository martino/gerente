import decimal
import grequests
import requests
import simplejson as json

from copy import copy
from django.conf import settings


class Datatxt(object):

    def __init__(self):
        # self.red = redis.StrictRedis(host='localhost', port=6379, db=3)
        self.default_params = {
            '$app_id': settings.APP_ID,
            '$app_key': settings.APP_KEY
        }

        self.urls = {
            'models': '{}/datatxt/cl/models/v1'.format(settings.DATATXT),
            'cl': '{}/datatxt/cl/v1'.format(settings.DATATXT),
            'nex': '{}/datatxt/nex/v1'.format(settings.DATATXT),
        }

    def create_model(self, model):
        if not isinstance(model, basestring):
            model = json.dumps(model, use_decimal=True)
        params = copy(self.default_params)
        params['data'] = model
        req = requests.post(self.urls['models'], data=params)
        return req

    def update_model(self, id, model):
        params = copy(self.default_params)
        params['data'] = model
        params['id'] = id
        req = requests.put(self.urls['models'], data=params)
        return req

    def delete_model(self, model_id):
        params = copy(self.default_params)
        params['id'] = model_id
        req = requests.delete(self.urls['models'], params=params)
        return req

    def nex(self, text, lang='it', use_grequests=False):
        params = copy(self.default_params)
        params['text'] = text
        params['lang'] = lang
        nex_url = self.urls['nex']
        if use_grequests:
            req = grequests.post(nex_url, data=params)
        else:
            req = requests.post(nex_url, data=params)
        return req

    def classify(self, model_id, text, use_grequests=False):
        params = copy(self.default_params)
        params['model'] = model_id
        params['text'] = text
        params['include'] = 'score_details'
        params['nex.min_confidence'] = 0.6
        if use_grequests:
            req = grequests.post(self.urls['cl'], data=params)
        else:
            req = requests.post(self.urls['cl'], data=params)
        return req
