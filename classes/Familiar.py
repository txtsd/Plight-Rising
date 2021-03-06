# ---------------------------------------------------------------------
# ------------------------- Plight Rising -----------------------------
# -----------------------------txtsd-----------------------------------
# ---------------------------------------------------------------------

"""Bonds with all familiars"""

# Imports -------------------------------------------------------------
import time
import datetime
import random
import re
import os
import sys
import requests
from configobj import ConfigObj
from validate import Validator
# End Imports ---------------------------------------------------------


class Familiar:

    def __init__(self, acc):
        self.acc = acc
        self.userid = acc.getID()
        self.derg = None
        self.configspec = ConfigObj('config.spec', encoding='UTF8', list_values=False)
        self.config = ConfigObj('config.ini', configspec=self.configspec)
        val = Validator()
        test = self.config.validate(val, preserve_errors=True)
        self.mindelay = self.config['account']['bond']['mindelay']
        self.maxdelay = self.config['account']['bond']['maxdelay']
        self.check = False
        self.tried = 0

    def prebond(self):

        self.check = False
        self.tried = 0
        while not self.check:
            if (self.tried < 3):
                try:
                    time.sleep(random.uniform(0.5, 2))
                    html = self.acc.get('/main.php',
                                        param={
                                            'p': 'lair',
                                            'id': self.userid,
                                        },
                                        referer='/main.php?p=hoard'
                                        )
                    self.check = True
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Prebond_1_error_pageload')
                    self.tried += 1
                    pass
            else:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                sys.exit()

        dragons = re.findall('did=(\d*)', html.text)

        numpages = re.findall('id=' + self.userid + '&page=(\d+)', html.text)
        if numpages:
            if len(numpages) >= 2:
                for i in range(2, len(numpages) + 1):
                    time.sleep(random.uniform(1, 3))

                    self.check = False
                    self.tried = 0
                    while not self.check:
                        if (self.tried < 3):
                            try:
                                htmld = self.acc.get('/main.php',
                                                     param={
                                                         'p': 'lair',
                                                         'id': self.userid,
                                                         'page': str(i),
                                                     },
                                                     referer='/main.php?p=lair&id=' + self.userid + '&page=' + str(i - 1)
                                                     )
                                self.check = True
                            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Prebond_2_error_dergcollect')
                                self.tried += 1
                                pass
                        else:
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                            sys.exit()

                    dragons += re.findall('did=(\d*)', htmld.text)

        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Begin Bonding!')
        self.derg = dragons[0]
        for x in dragons:
            time.sleep(random.uniform(self.mindelay, self.maxdelay))

            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    # print(x)
                    try:
                        html2 = self.acc.get('/main.php',
                                             param={
                                                 'p': 'lair',
                                                 'id': self.userid,
                                                 'tab': 'dragon',
                                                 'did': x,
                                             },
                                             referer='/main.php?p=lair&id=' + self.userid
                                             )
                        famID = re.search("bondJamesbond\(\'(\d*)", html2.text)
                        if famID:
                            time.sleep(random.uniform(self.mindelay, self.maxdelay))
                            html3 = self.acc.post('/includes/ol/fam_bonding.php',
                                                  data={
                                                      'id': famID.group(1),
                                                  },
                                                  head={
                                                      'Accept': '*/*',
                                                      'Accept-Encoding': 'gzip,deflate',
                                                      'X-Requested-With': 'XMLHttpRequest',
                                                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                                  },
                                                  referer='/main.php?p=lair&id=' +
                                                  self.userid + '&tab=dragon&did=' + x
                                                  )
                            self.check = True
                            # Have this ajaxlookup and print Names
                            # Parse for rewards
                            result = re.search("731d08;\">(.*?)</span>", html3.text)
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' +
                                  result.group(1).replace('â\x80\x99', "'").replace('Ã\xB6', "o") + " bonded!")
                            # if 'Death' in result.group(1):
                            #     print(result.group(1).encode())
                        else:
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Already Bonded ' + x + "'s familiar!")
                            self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Prebond_3_error_post')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()

        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Prebonding Complete!")

    def shuffle(self):

        self.check = False
        self.tried = 0
        while not self.check:
            if (self.tried < 3):
                try:
                    html = self.acc.get('/main.php',
                                        param={
                                            'p': 'lair',
                                            'id': self.userid,
                                            'tab': 'familiar',
                                            'did': self.derg,
                                        },
                                        referer='/main.php?p=lair&id=' +
                                        self.userid + '&tab=dragon&did=' + self.derg
                                        )
                    self.check = True
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Shuffle_1_error_pageload')
                    self.tried += 1
                    pass
            else:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                sys.exit()

        # List the familiars that need bonding
        familiars = re.findall("\"attachFamiliar\(\'(\d+)'", html.text)
        for x in familiars:

            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    try:
                        html2 = self.acc.get('/includes/familiar_active.php',
                                             param={
                                                 'id': self.derg,
                                                 'itm': x,
                                             },
                                             head={
                                                 'Accept': '*/*',
                                                 'X-Requested-With': 'XMLHttpRequest',
                                             },
                                             referer='/main.php?p=lair&id=' +
                                             self.userid + '&tab=familiar&did=' + self.derg
                                             )
                        html3 = self.acc.get('/includes/familiar_inv.php',
                                             head={
                                                 'Accept': '*/*',
                                                 'X-Requested-With': 'XMLHttpRequest',
                                             },
                                             referer='/main.php?p=lair&id=' +
                                             self.userid + '&tab=familiar&did=' + self.derg
                                             )
                        time.sleep(random.uniform(self.mindelay, self.maxdelay))
                        self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Shuffle_2_error_famswitch')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()

            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    # print(x)
                    try:
                        html4 = self.acc.get('/main.php',
                                             param={
                                                 'p': 'lair',
                                                 'id': self.userid,
                                                 'tab': 'dragon',
                                                 'did': self.derg,
                                             },
                                             referer='/main.php?p=lair&id=' +
                                             self.userid + '&tab=familiar&did=' + self.derg
                                             )
                        famID = re.search("bondJamesbond\(\'(\d*)", html4.text)
                        if famID:
                            time.sleep(random.uniform(self.mindelay, self.maxdelay))
                            html5 = self.acc.post('/includes/ol/fam_bonding.php',
                                                  data={
                                                      'id': x,
                                                  },
                                                  head={
                                                      'Accept': '*/*',
                                                      'Accept-Encoding': 'gzip,deflate',
                                                      'X-Requested-With': 'XMLHttpRequest',
                                                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                                  },
                                                  referer='/main.php?p=lair&id=' +
                                                  self.userid + '&tab=dragon&did=' + self.derg
                                                  )
                            self.check = True
                            # Have this ajaxlookup and print Names
                            # Parse for rewards
                            result = re.search("731d08;\">(.*?)</span>", html5.text)
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' +
                                  result.group(1).replace('â\x80\x99', "'").replace('Ã\xB6', "o") + " bonded!")
                            # if 'Death' in result.group(1):
                            #     print(result.group(1).encode())
                            time.sleep(random.uniform(self.mindelay, self.maxdelay))
                        else:
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Already Bonded with ' + x)
                            self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Shuffle_3_error_post')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()

            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    try:
                        html8 = self.acc.get('/main.php',
                                             param={
                                                 'p': 'lair',
                                                 'id': self.userid,
                                                 'tab': 'familiar',
                                                 'did': self.derg,
                                             },
                                             referer='/main.php?p=lair&id=' +
                                             self.userid + '&tab=dragon&did=' + self.derg
                                             )
                        self.check = True
                        time.sleep(random.uniform(self.mindelay, self.maxdelay))
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Shuffle_4_error_autopageload')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()

        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Done Bonding!")

    def bond(self):
        self.prebond()
        self.shuffle()
        os.system("pause")
