# ---------------------------------------------------------------------
# ------------------------- Plight Rising -----------------------------
# -----------------------------txtsd-----------------------------------
# ---------------------------------------------------------------------

"""Does gathering and Pinkerton and feeds your lair"""

# Imports -------------------------------------------------------------
import time
import datetime
import random
import re
import sys
import requests
from configobj import ConfigObj
from bs4 import BeautifulSoup as bs
# End Imports ---------------------------------------------------------


class Gather:

    def __init__(self, acc):
        self.acc = acc
        self.userID = acc.getID()
        self.config = ConfigObj('config.ini')
        self.area = {'earth': '1',
                     'plague': '2',
                     'wind': '3',
                     'water': '4',
                     'lightning': '5',
                     'ice': '6',
                     'shadow': '7',
                     'light': '8',
                     'arcane': '9',
                     'nature': '10',
                     'fire': '11'
                     }
        self.areachoice = self.area[self.config['account']['gather']['area']]
        self.action = self.config['account']['gather']['action']
        self.pinkerton = self.config['account']['pinkerton']
        self.feed = self.config['account']['feed']

    def getItems(self, html_):
        things = re.findall("<a rel=\"(.*?)\" class=\"clue\"[\s\S]*?>(\d+?)<\/div>", html_.text)
        for x in things:
            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    try:
                        html = self.acc.get('http://flightrising.com/' + x[0],
                                            head={
                                                'Accept': 'text/html, */*; q=0.01',
                                                'X-Requested-With': 'XMLHttpRequest',
                                            },
                                            referer='/main.php?p=gather&action=' + self.action
                                            )
                        self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_0_error_getItems')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()
            # info = re.findall(">([^\s].*?)<\/div>", html.text)
            # rating = re.search("tooltip_(\d*)star\.", html.text)
            soup = bs(html.text)
            strings = list(soup.stripped_strings)
            found = {}
            try:
                if (strings[1] == 'Food') or (strings[1] == 'Insect') or (strings[1] == 'Meat') or (strings[1] == 'Plant') or (strings[1] == 'Seafood'):
                    found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['subtype'] = strings[1]
                    found['desc'] = strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['cost'] = int(re.search("(\d+)", strings[3]).group(1))
                    found['fp'] = int(re.search("(\d+)", strings[4]).group(1))
                    found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                elif (strings[1] == 'Materials') or (strings[1] == 'Dragonmade Material') or (strings[1] == 'Minerals & Ores') or (strings[1] == 'Organic Material'):
                    if len(strings) == 3:
                        found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                        found['subtype'] = 'NIL'
                        found['desc'] = strings[1].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                        found['cost'] = int(re.search("(\d+)", strings[2]).group(1))
                        found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                    else:
                        found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                        found['subtype'] = strings[1]
                        found['desc'] = strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                        found['cost'] = int(re.search("(\d+)", strings[3]).group(1))
                        found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                elif strings[1] == 'Apparel':
                    found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['subtype'] = strings[1]
                    found['desc'] = strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['cost'] = int(re.search("(\d+)", strings[3]).group(1))
                    found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                elif strings[1] == 'Familiar':
                    found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['subtype'] = strings[1]
                    found['desc'] = strings[2].encode('utf8').decode('utf8').replace('\u2026', '...').replace('\u2019', "'") if re.search('\\u2019', strings[2]) else strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['cost'] = int(re.search("(\d+)", strings[3]).group(1))
                    found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                elif (strings[1] == 'Battle') or (strings[1] == 'Energy Stone') or (strings[1] == 'Battle Item') or (strings[1] == 'Augment Stone') or (strings[1] == 'Accessory Stone') or (strings[1] == 'Ability Stone'):
                    found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['subtype'] = strings[1]
                    found['desc'] = strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['cost'] = int(re.search("(\d+)", strings[3]).group(1))
                    found['level'] = int(re.search("(\d+)", strings[4]).group(1))
                    found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                elif strings[1] == 'Other':
                    found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['subtype'] = strings[1]
                    found['desc'] = strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['cost'] = int(re.search("(\d+)", strings[3]).group(1))
                    found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                elif strings[1] == 'Skins':
                    found['name'] = strings[0].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['subtype'] = strings[1]
                    found['desc'] = strings[2].encode('latin1').decode('utf8').replace('\u2026', '...').replace('\u2019', "'")
                    found['rating'] = int(re.search("tooltip_(\d+)star\.", html.text).group(1)) if re.search("tooltip_(\d+)star\.", html.text) else 0
                else:
                    print('New type of item found.')
            except:
                print("Derp", found)
            try:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + x[1] + ' [' + found['subtype'] + '] [' + found['name'] + ']')
                # for y in info:
                #     print(' [' + y + ']', end='')
                # print(' [Rating: ' + rating.group(1) + ']')
            except:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Unable to print.')
        if re.search("level_up.png", html_.text):
            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Your [" + self.action + "] leveled up!")
        print("-")

    def gather(self):
        self.check = False
        self.tried = 0
        while not self.check:
            if (self.tried < 3):
                try:
                    html = self.acc.get('/main.php',
                                        param={
                                            'p': 'gather'
                                        },
                                        referer='/main.php?p=hoard'
                                        )
                    self.check = True
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_1_error_pregather')
                    self.tried += 1
                    pass
            else:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                sys.exit()
        # Parse page, look for remaining turns
        turns = None
        turns = re.search("Turns Left Today:[\s\S]*?(\d+)[\s]*<\/div>", html.text)
        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Turns remaining today: ' + turns.group(1))
        if (int(turns.group(1)) > 0):
            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    try:
                        time.sleep(random.uniform(2, 4))
                        html2 = self.acc.post('/main.php',
                                              param={
                                                  'p': 'gather',
                                                  'action': self.action,
                                              },
                                              data={
                                                  'gather': self.areachoice,
                                              },
                                              head={
                                                  'Cache-Control': 'max-age=0',
                                              },
                                              referer='/main.php?p=gather'
                                              )
                        self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_2_error_first')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()
            # Look for and print acquired items and levelups
            self.getItems(html2)
            for x in range(0, int(turns.group(1)) - 1):
                self.check = False
                self.tried = 0
                while not self.check:
                    if (self.tried < 3):
                        try:
                            time.sleep(random.uniform(1, 2))
                            html3 = self.acc.post('/main.php',
                                                  param={
                                                      'p': 'gather',
                                                      'action': self.action,
                                                  },
                                                  data={
                                                      'gather': self.areachoice,
                                                  },
                                                  head={
                                                      'Cache-Control': 'max-age=0',
                                                  },
                                                  referer='/main.php?p=gather&action=' + self.action
                                                  )
                            self.check = True
                        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_3_error_subsequent')
                            self.tried += 1
                            pass
                    else:
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                        sys.exit()
                # Look for and print acquired items and levelups
                self.getItems(html3)
        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Done Gathering')

        # Pinkerton section
        if self.pinkerton:
            time.sleep(random.uniform(2, 4))
            print('\n' + '[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Visiting Pinkerton')
            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    try:
                        html4 = self.acc.get('/main.php',
                                             param={
                                                 'p': 'tradepost',
                                             },
                                             referer='/main.php?p=hoard'
                                             )
                        html5 = self.acc.get('/main.php',
                                             param={
                                                 'p': 'tradepost',
                                                 'lot': 'pile',
                                             },
                                             referer='/main.php?p=tradepost'
                                             )
                        self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_4_error_Pinkerton1')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()
            if re.search("disabled=\"disabled\"", html5.text):
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Already grabbed today's item.")
            else:
                time.sleep(random.uniform(2, 4))
                self.check = False
                self.tried = 0
                while not self.check:
                    if (self.tried < 3):
                        try:
                            html6 = self.acc.post('/includes/ol/ol_pinkpile.php',
                                                  head={
                                                      'Accept': '*/*',
                                                      'X-Requested-With': 'XMLHttpRequest',
                                                  },
                                                  referer='/main.php?p=tradepost&lot=pile'
                                                  )
                            self.check = True
                        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_5_error_Pinkerton1')
                            self.tried += 1
                            pass
                    else:
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                        sys.exit()
                link = re.search('<a rel=\"(.*?)\" class=\"clue\"[\s\S]*?>', html6.text)
                self.check = False
                self.tried = 0
                while not self.check:
                    if (self.tried < 3):
                        try:
                            html7 = self.acc.get('http://flightrising.com/' + link.group(1),
                                                 head={
                                                     'Accept': 'text/html, */*; q=0.01',
                                                     'X-Requested-With': 'XMLHttpRequest',
                                                 },
                                                 referer='/main.php?p=tradepost&lot=pile'
                                                 )
                            self.check = True
                        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_6_error_Pinkerton2')
                            self.tried += 1
                            pass
                    else:
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                        sys.exit()
                info = re.findall(">([^\s].*?)<\/div>", html7.text)
                rating = re.search("tooltip_(\d*)star\.", html7.text)
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ', end='')
                for x in info:
                    print('[' + x + '] ', end='')
                print(' [Rating: ' + rating.group(1) + ']')
            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Done Pinking\n")

        # Feeding section
        if self.feed:
            time.sleep(random.uniform(2, 4))
            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Feeding dergs')
            self.check = False
            self.tried = 0
            while not self.check:
                if (self.tried < 3):
                    try:
                        html8 = self.acc.post('/includes/ol/feed.php',
                                              head={
                                                  'Accept': '*/*',
                                                  'X-Requested-With': 'XMLHttpRequest',
                                              },
                                              referer='/main.php?p=lair&id=' + self.userID
                                              )
                        self.check = True
                    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Gather_7_error_Feed')
                        self.tried += 1
                        pass
                else:
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                    sys.exit()
            print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Done Feeding\n")
