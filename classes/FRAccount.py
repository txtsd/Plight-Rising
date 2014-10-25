# ---------------------------------------------------------------------
# ------------------------- Plight Rising -----------------------------
# -----------------------------txtsd-----------------------------------
# ---------------------------------------------------------------------

"""Handles the account, login, and connections"""

# Imports -------------------------------------------------------------
import time
import datetime
import pickle
import re
import os
import sys
import requests
from configobj import ConfigObj
# End Imports ---------------------------------------------------------


class FRAccount:

    config = ConfigObj('config.ini')
    domain = 'http://flightrising.com'
    headers = {
        'User-Agent': config['account']['useragent'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'DNT': '1' if config['account']['DNT'] == 'true' else None
        }

    def __init__(self, un, pw, proxy=""):
        self.un = un
        self.pw = pw
        self.proxy = proxy
        self.referrer = None
        self.result = None
        self.ID = None
        self.cookies = None

        if os.path.isfile(self.un + '.bin'):
            with open(self.un + '.bin', 'rb') as f:
                self.session = pickle.load(f)
        else:
            self.session = requests.Session()
        a = requests.adapters.HTTPAdapter(max_retries=0)
        self.session.mount('http://', a)
        self.session.headers = self.headers

        if (self.proxy != ""):
            self.session.proxies = {'http': 'http://' + self.proxy + '/'}

    def get(self, url, param={}, referer='', head={}):
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            head['Referer'] = referer
        self.result = self.session.get(url, params=param, headers=head, timeout=90)
        return self.result

    def post(self, url, data={}, param={}, referer='', head={}):
        head['Origin'] = 'http://flightrising.com'
        if url[0] == '/':
            url = self.domain + url
        if referer != '':
            if referer[0] == '/':
                referer = self.domain + referer
            head['Referer'] = referer
        self.result = self.session.post(url, params=param, data=data, headers=head, timeout=90)
        return self.result

    def login(self):
        try:
            self.result = self.session.get('http://www1.flightrising.com/', timeout=90)
            if re.search(self.un, self.result.text):
                self.result2 = self.session.get('http://flightrising.com/main.php',
                                                params={
                                                    'p': 'hoard',
                                                },
                                                headers={
                                                    'Referer': 'http://www1.flightrising.com/'
                                                },
                                                timeout=90
                                                )
                if re.search(self.un, self.result2.text):
                    # self.ID = self.session.cookies['userid']
                    self.ID = re.search('clan-profile\/(\d+)">Clan Profile', self.result.text).group(1)
                    print(
                        '\n[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Already logged in!')
                    return True
            # print('beforepoop')
            token = re.search('"hidden" value="(.+?)"', self.result.text).group(1)
            # print('afterpoop')
            self.result = self.session.post('https://www1.flightrising.com/login/login',
                                            headers={
                                                # 'Referer': 'http://flightrising.com/main.php?p=coliseum',
                                                'Referer': 'http://www1.flightrising.com/',
                                                # 'Accept': '*/*',
                                                # 'X-Requested-With': 'XMLHttpRequest',
                                                'X-Request-Id': None,
                                                # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                                'Origin': 'http://www1.flightrising.com',
                                                'Cache-Control': 'max-age=0'
                                            },
                                            data={
                                                '_token': token,
                                                'uname': self.un,
                                                'remember': '1',
                                                'pword': self.pw,
                                                # 'dologin': 'Login'
                                            },
                                            timeout=90
                                            )
            # self.result2 = self.session.get('http://flightrising.com/main.php?p=coliseum',
            #                                 headers={
            #                                     'Referer': 'http://flightrising.com/main.php?p=coliseum'
            #                                 },
            #                                 timeout=90
            #                                 )
            # print(self.result.url)
            # if re.search('Logging in...', self.result.text):
            if re.search('badpw=true', self.result.url):
                print('\n[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad Password Error.')
                return False
            if re.search('maint=true', self.result.url):
                print('\n[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Maintenance Error.')
                return False
            if re.search(self.un, self.result.text):
                # self.ID = self.result.cookies['userid']
                self.ID = re.search('clan-profile\/(\d+)">Clan Profile', self.result.text).group(1)
                print('\n[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Logged in!')
                if os.path.isfile(self.un + '.bin'):
                    os.remove(self.un + '.bin')
                with open(self.un + '.bin', 'wb') as f:
                    pickle.dump(self.session, f, pickle.HIGHEST_PROTOCOL)
                return True
            else:
                print(
                    '\n[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Authorization Error.')
                return False
        except Exception as e:
            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Network Error.')
            print(type(e))
            print(e.args)
            print(e)
            time.sleep(10)

    def getID(self):
        return self.ID
