# ---------------------------------------------------------------------
# ------------------------- Plight Rising -----------------------------
# -----------------------------txtsd-----------------------------------
# ---------------------------------------------------------------------

"""Plays Coliseum for you"""

# Imports -------------------------------------------------------------
import asyncio
import json
import re
import time
import random
import datetime
import sys
import math
import os
import requests
from configobj import ConfigObj
from autobahn.asyncio.websocket import WebSocketClientProtocol
from autobahn.asyncio.websocket import WebSocketClientFactory
# End Imports ---------------------------------------------------------


class Coliseum(WebSocketClientProtocol):

    longthing = None
    userid = None

    def __init__(self):
        self.acc = None
        self.config = ConfigObj('config.ini')
        self.mindelay = self.config['account']['coliseum']['mindelay']
        self.maxdelay = self.config['account']['coliseum']['maxdelay']
        self.train = self.config['account']['coliseum']['trainingmode']
        self.trainpos = self.config['account']['coliseum']['trainingpos']
        self.debuglog = self.config['account']['coliseum']['debuglog']
        self.dec = json.JSONDecoder()
        self.wskey = None
        self.connection = None
        self.thing = None
        self.fb = None
        self.fa = None
        self.enemyList = []
        self.readyToFight = 0
        self.warning = 0
        self.loop = asyncio.get_event_loop()
        self.headers = {'Origin': 'http://flightrising.com',
                        'Accept-Encoding': 'gzip,deflate,sdch',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'DNT': '1' if self.config['account']['DNT'] else None
                        }
        self.useragent = self.config['account']['useragent']
        # training_fields, woodland_border, scorched_forest, sandswept_delta, forgotten_cave,
        # bamboo_waterfall, waterway, arena, boreal_wood, harpys_roost, mire, kelp_beds
        self.area = self.config['account']['coliseum']['area']
        self.order = {'1': 13, '2': 15, '3': 240, '4': 10, '5': 30, '6': 50, '7': 80, '8': 10, '9': 80, '10': 20,
                      '11': 110, '12': 70, '13': 11, '14': 16, '15': 6, '16': 8, '17': 12, '18': 10, '19': 70, '20': 150,
                      '21': 140, '22': 17, '23': 23, '24': 130, '25': 18, '26': 100, '27': 20, '28': 220, '29': 140, '30': 30,
                      '31': 70, '32': 60, '33': 34, '34': 30, '35': 32, '36': 70, '37': 50, '38': 230, '39': 210, '40': 19,
                      '41': 35, '42': 30, '43': 33, '44': 60, '45': 60, '46': 70, '47': 40, '48': 200, '49': 60, '50': 40,
                      '51': 20, '52': 31, '53': 70, '54': 20, '55': 29, '56': 160, '57': 190, '58': 80, '59': 90, '60': 110,
                      '61': 120, '62': 170, '63': 50, '64': 110, '65': 120, '66': 24, '67': 25, '68': 220, '69': 210, '70': 100,
                      '71': 130, '72': 20, '73': 60, '74': 80, '75': 10, '76': 50, '77': 80, '78': 110, '79': 50, '80': 30,
                      '81': 100, '82': 90, '83': 666, '84': 50, '85': 22, '86': 30, '87': 70, '88': 20, '89': 60, '90': 100, '91': 130,
                      '92': 3, '93': 7, '94': 50, '95': 40, '96': 30, '97': 60, '98': 100, '99': 90, '100': 120, '101': 90,
                      '102': 115, '103': 30, '104': 40, '105': 110, '106': 130, '107': 70, '108': 100, '109': 20, '110': 10, '111': 60,
                      '112': 50, '113': 80, '114': 90, '115': 120, '116': 40, '117': 28, '118': 2, '119': 1, '120': 10, '121': 20,
                      '122': 150, '123': 160, '124': 30, '125': 10, '126': 40, '127': 10, '128': 9, '129': 5, '130': 4, '131': 40,
                      '132': 20, '133': 40, '134': 110, '135': 70, '136': 20, '137': 100, '138': 90, '139': 10, '140': 60, '141': 50,
                      '142': 120, '143': 80, '144': 40, '145': 30, '146': 21, '147': 14, '148': 27, '149': 26, '150': 220, '151': 210,
                      '152': 194, '153': 195, '154': 10, '155': 90, '156': 130, '157': 140, '158': 666, '159': 666, '160': 666,
                      '161': 666, '162': 666, '163': 666, '164': 666, '165': 666, '166': 666, '167': 666, '168': 666, '169': 666, '170': 666,
                      '171': 666, '172': 666, '173': 666, '174': 666, '175': 666, '176': 666, '177': 666, '178': 666, '179': 666, '180': 666,
                      '181': 666, '182': 666, '183': 666, '184': 666, '185': 666, '186': 666, '187': 666, '188': 666, '189': 666, '190': 666,
                      '191': 666, '192': 666, '193': 666, '194': 666, '195': 666, '196': 666, '197': 666, '198': 666, '199': 666, '200': 666
                      }

    def play(self, acc):
        self.acc = acc
        self.loop = asyncio.get_event_loop()
        Coliseum.userid = acc.getID()
        time.sleep(random.uniform(1, 2))
        self.check = False
        self.tried = 0
        while not self.check:
            if (self.tried < 3):
                try:
                    html = self.acc.get('/main.php',
                                        param={
                                            'p': 'coliseum',
                                        },
                                        referer='/main.php?p=coliseum')
                    self.check = True
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Coli_1_error')
                    self.tried += 1
                    time.sleep(random.uniform(1, 2))
                    pass
            else:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                sys.exit()
        time.sleep(random.uniform(1, 2))
        # print('lenhtml:', len(html.text))
        # print('test')
        self.check = False
        self.tried = 0
        while not self.check:
            if (self.tried < 3):
                try:
                    html2 = self.acc.get('http://207.58.158.212:4231/coliseum0/socket.io/1/',
                                         param={
                                             't': str(int(time.time() * 1000)),
                                         },
                                         head={
                                             'Accept': '*/*',
                                             'Origin': 'http://flightrising.com',
                                         },
                                         referer='/main.php?p=coliseum'
                                         )
                    self.check = True
                except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                    print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Coli_2_error')
                    self.tried += 1
                    time.sleep(random.uniform(1, 2))
                    pass
            else:
                print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + 'Bad network. Try again later.')
                sys.exit()
        # print('lenhtml2:', len(html2.text))
        # print('test2')
        if (html2.status_code == requests.codes.ok):
            temp = re.search('(.*):60:60:websocket', html2.text)
            # print('test3')
            self.wskey = temp.group(1)
            # print('test4')
            self.connection = re.search('(\w+) = io\.connect', html.text).group(1)
            # print('test5')
            self.thing = re.search('(\w+) = \'JMxc-w-wd2DQ\'', html.text).group(1)
            # print('test6')
            Coliseum.longthing = re.search(self.connection + "\.emit\(" + self.thing + "\, \'(.*?)\'\)\;", html.text).group(1)
            # print('test7')

            if self.debuglog:
                with open(Coliseum.userid + '.log', 'a') as p:
                    p.write('\n' + "Beginning WebSocket operations" + '\n')
                    p.write(self.wskey + '\n')
                    p.write(self.connection + '\n')
                    p.write(self.thing + '\n')
                    p.write(Coliseum.longthing + '\n')

            factory = WebSocketClientFactory("ws://207.58.158.212:4231/coliseum0/socket.io/1/websocket/" + self.wskey,
                                             debug=False,
                                             headers=self.headers,
                                             useragent=self.useragent
                                             )
            factory.protocol = Coliseum

            coro = self.loop.create_connection(factory, '207.58.158.212', 4231)
            try:
                self.loop.run_until_complete(coro)
                self.loop.run_forever()
            # except:
            #     pass
            finally:
                self.loop.stop()
                # self.loop.close()
                return
        elif not (html2.status_code == requests.codes.ok):
            # print('Not 200.')
            print(html2.status_code)
        else:
            print("Derp.")

    def onConnect(self, response):
        print('-----------------------------------------------------------------------')
        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "Server connected: {0}".format(response.peer))

    def onOpen(self):
        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        try:
            received = payload.decode('utf-8')
            if self.debuglog:
                # print("<- {}".format(received[:80]))
                with open(Coliseum.userid + '.log', 'a') as p:
                    p.write("<- {}".format(received) + '\n')
            if (received[:3] == '2::'):
                self.sendMessage('2::'.encode('utf-8'))
                if self.debuglog:
                    # print("-> {}".format('2::'))
                    with open(Coliseum.userid + '.log', 'a') as p:
                        p.write("-> {}".format('2::') + '\n')
            elif (received[:3] == "1::"):
                pass
            elif (received[:4] == '5:::'):
                msgpre = received[4:]
                msg = self.dec.decode(msgpre)
                if (msg['name'] == 'gotoTitle'):
                    go = {"name": "coliseum_beginBattle", "args": [{"venue": self.area}]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                    if self.debuglog:
                        # print("-> {}".format(goforth))
                        with open(Coliseum.userid + '.log', 'a') as p:
                            p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'l20rj2f2f'):
                    go = {"name": "JMxc-w-wd2DQ", "args": [Coliseum.longthing]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.sendMessage(goforth.encode('utf-8'))
                    if self.debuglog:
                        # print("-> {}".format(goforth))
                        with open(Coliseum.userid + '.log', 'a') as p:
                            p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'finalizeBattle'):
                    self.fb = msg
                    teamHP = 0
                    teamMaxHP = 0
                    self.warning = 0
                    dergcount = 0
                    for i, d in enumerate(self.fb['args'][0]['playerSet']):
                        try:
                            dergcount += 1
                            teamHP += float(d['health'])
                            teamMaxHP += float(d['maxHP'])
                            if (teamHP < (teamMaxHP * 0.25)):
                                print("[--Warning--] Team HP lower than 25%. Aborting.")
                                if self.debuglog:
                                    with open(Coliseum.userid + '.log', 'a') as p:
                                        p.write("----- {}".format("Team HP lower than 25%.") + '\n')
                                self.loop.stop()
                                # self.loop.close()
                            if (d['a5'] == 674):
                                self.fb['args'][0]['playerSet'][i]['strength'] += 5
                                self.fb['args'][0]['playerSet'][i]['quickness'] += 3
                                self.fb['args'][0]['playerSet'][i]['agility'] += 1
                            if (d['a6'] == 674):
                                self.fb['args'][0]['playerSet'][i]['strength'] += 5
                                self.fb['args'][0]['playerSet'][i]['quickness'] += 3
                                self.fb['args'][0]['playerSet'][i]['agility'] += 1
                            if (d['a7'] == 674):
                                self.fb['args'][0]['playerSet'][i]['strength'] += 5
                                self.fb['args'][0]['playerSet'][i]['quickness'] += 3
                                self.fb['args'][0]['playerSet'][i]['agility'] += 1
                        except:
                            print("[--Warning--] Less than 3 dergs in party. Rectify.")
                            if self.debuglog:
                                with open(Coliseum.userid + '.log', 'a') as p:
                                    p.write("----- {}".format("Less than 3 dragons in party.") + '\n')
                            self.loop.stop()
                            # self.loop.close()
                            os.system("pause")
                    # This bit probably doesn't work since it the 3rd dragon entry exists anyway.
                    if (dergcount < 3):
                        print("[--Warning--] Less than 3 dergs in party. Rectify.")
                        if self.debuglog:
                            with open(Coliseum.userid + '.log', 'a') as p:
                                p.write("----- {}".format("Less than 3 dragons in party.") + '\n')
                        self.loop.stop()
                        # self.loop.close()
                        os.system("pause")
                    self.bId = msg['args'][0]['battleId']
                    go = {"name": "coliseum_battleLoaded",
                          "args": [{"battleId": self.bId, "user": Coliseum.userid}]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                    if self.debuglog:
                        # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), print, "-> {}".format(goforth))
                        with open(Coliseum.userid + '.log', 'a') as p:
                            p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'loadedIn'):
                    if not re.search('^e\d+x+', str(self.fb['args'][0]['turnArray'][0]['id'])):
                        self.derg = self.fb['args'][0]['turnArray'][0]
                        for e in self.fb['args'][0]['enemySet']:
                            if not self.enemyList:
                                self.enemyList.append(e)
                            else:
                                for i, y in enumerate(self.enemyList):
                                    if self.order[str(e['realid'])] <= self.order[str(y['realid'])]:
                                        self.enemyList.insert(i, e)
                                        break
                                    else:
                                        self.enemyList.append(e)
                                        break
                        go = {"name": "coliseum_useAbility"}
                        if self.derg['breath'] < 35:
                            go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                           "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                           "ability": "1", "abilityId": str(random.randint(111, 999)),
                                           "battleId": self.bId,
                                           "aoeTargets": []}
                                          ]
                        if self.derg['breath'] >= 35:
                            if (self.getScratch(self.derg, self.enemyList[0]) >= self.enemyList[0]['health']):
                                go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                               "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                               "ability": "1", "abilityId": str(random.randint(111, 999)),
                                               "battleId": self.bId,
                                               "aoeTargets": []}
                                              ]
                            elif (self.getEliminate(self.derg, self.enemyList[0]) >= self.enemyList[0]['health']):
                                go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                               "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                               "ability": "4", "abilityId": str(random.randint(111, 999)),
                                               "battleId": self.bId,
                                               "aoeTargets": []}
                                              ]
                            else:
                                go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                               "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                               "ability": "1", "abilityId": str(random.randint(111, 999)),
                                               "battleId": self.bId,
                                               "aoeTargets": []}
                                              ]
                        goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                        self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                        if self.debuglog:
                            # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), print, "-> {}".format(goforth))
                            with open(Coliseum.userid + '.log', 'a') as p:
                                p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'finalizeAbility'):
                    self.fa = msg
                    if not self.fa['args'][0]['newTurns'] == 0:
                        if not re.search('^e\d+x+', str(self.fa['args'][0]['newTurns']['array'][0]['id'])):
                            if self.enemyList:
                                # for d in self.fa['args'][0]['newTurns']['array']:
                                #     if ((float(d['health']) < float((d['maxHP'])*0.25)) and d['team'] == 1):
                                #         self.loop.stop()
                                #         self.loop.close()
                                #         sys.exit()
                                for i, x in enumerate(self.fb['args'][0]['enemySet']):
                                    if x['id'] == self.fa['args'][0]['target']:
                                        self.fb['args'][0]['enemySet'][i]['health'] -= self.fa['args'][0]['damage']
                                        # print(str(self.fb['args'][0]['enemySet'][i]['id']) + ' ' + str(self.fb['args'][0]['enemySet'][i]['health']))
                                self.derg = self.fa['args'][0]['newTurns']['array'][0]
                                go = {"name": "coliseum_useAbility"}
                                if self.derg['breath'] < 35:
                                    go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                                   "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                                   "ability": "1", "abilityId": str(random.randint(111, 999)),
                                                   "battleId": self.bId,
                                                   "aoeTargets": []}
                                                  ]
                                if self.derg['breath'] >= 35:
                                    if (self.getScratch(self.derg, self.enemyList[0]) >= self.enemyList[0]['health']):
                                        go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                                       "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                                       "ability": "1", "abilityId": str(random.randint(111, 999)),
                                                       "battleId": self.bId,
                                                       "aoeTargets": []}
                                                      ]
                                    elif (self.getEliminate(self.derg, self.enemyList[0]) >= self.enemyList[0]['health']):
                                        go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                                       "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                                       "ability": "4", "abilityId": str(random.randint(111, 999)),
                                                       "battleId": self.bId,
                                                       "aoeTargets": []}
                                                      ]
                                    else:
                                        go["args"] = [{"caster": {"id": self.derg['id'], "ai": "0"},
                                                       "target": {"id": self.enemyList[0]['id'], "ai": self.enemyList[0]['ai']},
                                                       "ability": "1", "abilityId": str(random.randint(111, 999)),
                                                       "battleId": self.bId,
                                                       "aoeTargets": []}
                                                      ]
                                goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                                self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                                if self.debuglog:
                                    # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), print, "-> {}".format(goforth))
                                    with open(Coliseum.userid + '.log', 'a') as p:
                                        p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == "death"):
                    if self.enemyList:
                        if (self.enemyList[0]['id'] == msg['args'][0]):
                            self.enemyList.pop(0)
                        else:
                            for x in self.fb['args'][0]['playerSet']:
                                if (x['id'] == msg['args'][0]):
                                    self.warning += 1
                                    print("[--Warning--] " + str(msg['args'][0]) + " died.")
                                    if (self.warning >= 2):
                                        print("[--Warning--] Second derg died. Aborting.")
                                        if self.debuglog:
                                            with open(Coliseum.userid + '.log', 'a') as p:
                                                p.write("----- {}".format("2 dragons dead.") + '\n')
                                        self.warning = 0
                                        self.loop.stop()
                                        # self.loop.close()
                elif (msg['name'] == 'winBattle'):

                    ### Add data to file ###
                    if self.fb:
                        data = {}
                        data['time'] = time.time()
                        data['venue'] = self.fb['args'][0]['venue']
                        data['enemies'] = []
                        for i, g in enumerate(self.fb['args'][0]['enemySet']):
                            data['enemies'].append({})
                            data['enemies'][i]['realid'] = g['realid']
                            data['enemies'][i]['name'] = g['name']
                            data['enemies'][i]['element'] = g['element']
                        data['loot'] = []
                        for i, h in enumerate(msg['args'][0]['loot']):
                            data['loot'].append({})
                            data['loot'][i]['id'] = h['id']
                            data['loot'][i]['name'] = h['name']
                            data['loot'][i]['value'] = h['value']
                            data['loot'][i]['rarity'] = h['rarity']
                            data['loot'][i]['subtype'] = h['subtype']
                        with open(Coliseum.userid + '.txt', 'a') as f:
                            json.dump(data, f, separators=(',', ':'))
                            f.write('\n')
                    ### End adding data to file ###

                    if self.train:
                        print("[Level]", str(self.fb['args'][0]['playerSet'][self.trainpos]['level']),
                              " [Exp]", str(self.fb['args'][0]['playerSet'][self.trainpos]['xp_now']))
                    self.derg = None
                    self.enemyList = []
                    self.fb = None
                    self.fa = None
                    self.warning = 0
                    for e in msg['args'][0]['loot']:
                        print('[' + e['subtype'] + '] [' + e['name'].replace('\u2019', "'") + ']')
                    print('-----                    [' + str(datetime.datetime.now().time())[:-3] + ']')
                    go = {"name": "coliseum_beginBattle", "args": [{"venue": self.area}]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                    if self.debuglog:
                        # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), print, "-> {}".format(goforth))
                        with open(Coliseum.userid + '.log', 'a') as p:
                            p.write("-> {}".format(goforth) + '\n')
        except KeyboardInterrupt:
            sys.exit()

    def onClose(self, wasClean, code, reason):
        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "WebSocket connection closed: {0}".format(reason))
        # sys.exit()
        self.loop.stop()
        # self.loop.close()
        sys.exit()

    def getScratch(self, attacker, defender):
        return ((4 * attacker['strength'] + 12) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3)))

    def getBite(self, attacker, defender):
        return ((4 * attacker['strength'] + 12) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3)))

    def getShred(self, attacker, defender):
        return ((4 * attacker['strength'] + 17) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3)))

    def getShredDOT(self, attacker, defender):
        pass

    def getShredCritDOT(self, attacker, defender):
        pass

    def getSap(self, attacker, defender):
        return ((4 * attacker['strength'] + 15) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3)))

    def getSapLeech(self, attacker, defender):
        pass

    def getSapCritLeech(self, attacker, defender):
        pass

    def getElementalSlash(self, attacker, defender):
        elemult = Coliseum.getElementalMultiplier(attacker, defender)
        return (elemult * ((4 * attacker['strength'] + 75) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3))))

    def getElementalMultiplier(attacker, defender):
        multable = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0.5, 1, 0.5, 1, 2, 1, 1, 1, 2, 1, 2],
                    [1, 1, 0.5, 1, 2, 1, 1, 2, 0.5, 1, 2, 1],
                    [1, 2, 1, 0.5, 0.5, 2, 1, 1, 1, 2, 1, 1],
                    [1, 2, 1, 2, 0.5, 1, 0.5, 1, 1, 1, 1, 2],
                    [1, 1, 1, 1, 2, 0.5, 2, 1, 2, 0.5, 1, 1],
                    [1, 1, 2, 1, 2, 1, 0.5, 0.5, 1, 1, 2, 1],
                    [1, 1, 0.5, 2, 1, 1, 2, 0.5, 1, 1, 1, 2],
                    [1, 1, 2, 2, 1, 0.5, 1, 2, 0.5, 1, 1, 1],
                    [1, 1, 1, 1, 1, 2, 1, 2, 2, 0.5, 0.5, 1],
                    [1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 0.5],
                    [1, 0.5, 2, 1, 1, 1, 2, 1, 1, 1, 2, 0.5]
                    ]
        return multable[int(attacker['element'])][int(defender['element'])]

    def getClobber(self, attacker, defender):
        return ((4 * attacker['strength'] + 4) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3)))

    def getEliminate(self, attacker, defender):
        return (12 * attacker['strength'] + 75 - (4 * defender['defense']))

    def getContuse(self, attacker, defender):
        return ((4 * attacker['intellect'] + 19) - (math.floor(defender['mind'] / 3.) * 4 + (defender['mind'] % 3)))

    def getElementalBolt(self, attacker, defender):
        elemult = Coliseum.getElementalMultiplier(self, attacker, defender)
        return (elemult * ((4 * attacker['intellect'] + 75) - (math.floor(defender['mind'] / 3.) * 4 + (defender['mind'] % 3))))

    def getElementalUltimate(self, attacker, defender):
        elemult = Coliseum.getElementalMultiplier(attacker, defender)
        return (elemult * (6 * attacker['intellect'] + 17) - (2 * defender['mind']))

    def getEnvenomDOT(self, attacker, defender):
        # check
        return ((attacker['intellect'] * 10 + 20) / 5.)

    def getEnfeeble(self, attacker, defender):
        elemult = Coliseum.getElementalMultiplier(attacker, defender)
        return (elemult * ((2 * attacker['intellect'] + 100) - math.floor(defender['mind'] / 3.) * 2 + math.round((defender['mind'] % 3) / 3.)))
