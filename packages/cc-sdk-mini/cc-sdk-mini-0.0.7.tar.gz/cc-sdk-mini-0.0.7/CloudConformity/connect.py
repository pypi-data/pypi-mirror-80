#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import requests
import json
import urllib3
import time
from CloudConformity.__version__ import __version__
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Connection:
    def __init__(self, config):
        self._config = config
        self._session = None
        self._retries = 0
        self._MAX_RETRIES = 12
    def _buildheaders(self):
        return { 'Authorization': 'ApiKey ' + self._config.api_key,
                               'Content-Type': 'application/vnd.api+json',
                 'User-Agent': 'cc-sdk-mini ' + __version__ }
    def _setupSession(self):
        self._retries = 0
        if self._session is None:
            self._session = requests.Session()
            self._session .headers.update(self._buildheaders())
        return
    def patch(self, url, data, params=None):
        self._setupSession()
        resp = self._session.patch(self._config.host + url, json=data, params=params)
        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 202:
            return json.loads(resp.content.decode('utf-8'))
        elif resp.status_code == 204:
            return {'Status': "Successful",
                    'Code': resp.status_code}
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2 ** (self._retries + 3)) / 1000
            time.sleep(exp_backoff)
            self.get(url=url, params=params)
        return resp
    def get(self, url, params=None):
        self._setupSession()
        resp = self._session.get(self._config.host + url,  params=params)
        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 202:
            return json.loads(resp.content.decode('utf-8'))
        elif resp.status_code == 204:
            return {'Status': "Successful",
                    'Code': resp.status_code}
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.get(url=url, params=params)
        return resp

    def delete(self, url,  params=None):
        self._setupSession()
        resp = self._session.delete(self._config.host + url,  params=params)
        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 202 or resp.status_code == 204:
            return {'Status': "Successful",
                    'Code': resp.status_code}
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.delete(url=url, params=params)
        return resp

    def post(self, url, data,  params=None):
        self._setupSession()
        resp = self._session.post(self._config.host + url,  json=data, params=params)
        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 202:
            return json.loads(resp.content.decode('utf-8'))
        elif resp.status_code == 204:
            return {'Status': "Successful",
                    'Code': resp.status_code}
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.post(ur=url, data=data, params=params)
        return resp

    def put(self, url, data,  params=None):
        self._setupSession()
        resp = self._session.put(self._config.host + url,  json=data, params=params)
        if resp.status_code == 200 or resp.status_code == 201 or resp.status_code == 202:
            return json.loads(resp.content.decode('utf-8'))
        elif resp.status_code == 204:
            return {'Status': "Successful",
                    'Code': resp.status_code}
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.put(url=url, data=data, params=params)
        return resp