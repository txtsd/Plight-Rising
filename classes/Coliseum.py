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
        self.mindelay = float(self.config['account']['coliseum']['mindelay'])
        self.maxdelay = float(self.config['account']['coliseum']['maxdelay'])
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
                        'DNT': '1' if self.config['account']['DNT'] == 'true' else None
                        }
        self.useragent = self.config['account']['useragent']
        # training_fields, woodland_border, scorched_forest, sandswept_delta, forgotten_cave,
        # bamboo_waterfall, waterway, arena, boreal_wood, harpys_roost, mire, kelp_beds
        self.area = self.config['account']['coliseum']['area']
        self.order = {'1': 14, '2': 15, '3': 55, '4': 45, '5': 47, '6': 59, '7': 62, '8': 92, '9': 99, '10': 108,
                      '11': 101, '12': 98, '13': 11, '14': 13, '15': 6, '16': 8, '17': 12, '18': 67, '19': 73, '20': 81,
                      '21': 80, '22': 16, '23': 21, '24': 79, '25': 17, '26': 76, '27': 19, '28': 53, '29': 105, '30': 84,
                      '31': 88, '32': 87, '33': 31, '34': 135, '35': 29, '36': 51, '37': 49, '38': 54, '39': 52, '40': 18,
                      '41': 22, '42': 26, '43': 30, '44': 112, '45': 72, '46': 113, '47': 70, '48': 32, '49': 50, '50': 48,
                      '51': 46, '52': 28, '53': 61, '54': 56, '55': 25, '56': 40, '57': 42, '58': 74, '59': 75, '60': 77,
                      '61': 78, '62': 41, '63': 111, '64': 64, '65': 65, '66': 24, '67': 27, '68': 43, '69': 44, '70': 63,
                      '71': 66, '72': 34, '73': 38, '74': 89, '75': 82, '76': 86, '77': 114, '78': 117, '79': 71, '80': 69,
                      '81': 91, '82': 90, '83': 666, '84': 96, '85': 20, '86': 35, '87': 39, '88': 93, '89': 97, '90': 100,
                      '91': 104, '92': 3, '93': 7, '94': 37, '95': 36, '96': 57, '97': 60, '98': 116, '99': 115, '100': 103,
                      '101': 106, '102': 102, '103': 122, '104': 123, '105': 130, '106': 132, '107': 126, '108': 129, '109': 121, '110': 120,
                      '111': 125, '112': 124, '113': 127, '114': 128, '115': 131, '116': 58, '117': 23, '118': 2, '119': 1, '120': 33,
                      '121': 68, '122': 118, '123': 119, '124': 109, '125': 107, '126': 110, '127': 10, '128': 9, '129': 5, '130': 4,
                      '131': 85, '132': 83, '133': 136, '134': 143, '135': 139, '136': 134, '137': 142, '138': 141, '139': 133, '140': 138,
                      '141': 137, '142': 144, '143': 140, '144': 95, '145': 94, '146': 666, '147': 666, '148': 666, '149': 666, '150': 666,
                      '151': 666, '152': 666, '153': 666, '154': 666, '155': 666, '156': 666, '157': 666, '158': 666, '159': 666, '160': 666,
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
        html = self.acc.get('/main.php',
                            param={
                                'p': 'coliseum',
                            },
                            referer='/main.php?p=coliseum')
        time.sleep(random.uniform(1, 2))
        # print('lenhtml:', len(html.text))
        # print('test')
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

            # print("Beginning WebSocket operations")
            # print(self.wskey)
            # print(self.connection)
            # print(self.thing)
            # print(Coliseum.longthing, '\n')

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
                self.loop.close()
                self.loop.stop()
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
            # print("<- {}".format(received[:80]))
            # with open(Coliseum.userid + '.log', 'a') as p:
            #     p.write("<- {}".format(received) + '\n')
            if (received[:3] == '2::'):
                self.sendMessage('2::'.encode('utf-8'))
                # print("-> {}".format('2::'))
                # with open(Coliseum.userid + '.log', 'a') as p:
                #     p.write("-> {}".format('2::') + '\n')
            elif (received[:3] == "1::"):
                pass
            elif (received[:4] == '5:::'):
                msgpre = received[4:]
                msg = self.dec.decode(msgpre)
                delay = random.uniform(self.mindelay, float(self.config['account']['coliseum']['maxdelay']))
                if (msg['name'] == 'gotoTitle'):
                    go = {"name": "coliseum_beginBattle", "args": [{"venue": self.area}]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                    # print("-> {}".format(goforth))
                    # with open(Coliseum.userid + '.log', 'a') as p:
                    #     p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'l20rj2f2f'):
                    go = {"name": "JMxc-w-wd2DQ", "args": [Coliseum.longthing]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.sendMessage(goforth.encode('utf-8'))
                    # print("-> {}".format(goforth))
                    # with open(Coliseum.userid + '.log', 'a') as p:
                    #     p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'finalizeBattle'):
                    self.fb = msg
                    teamHP = 0
                    teamMaxHP = 0
                    self.warning = 0
                    dergcount = 0
                    for i, d in enumerate(self.fb['args'][0]['playerSet']):
                        dergcount += 1
                        teamHP += float(d['health'])
                        teamMaxHP += float(d['maxHP'])
                        if (teamHP < (teamMaxHP * 0.25)):
                            print("[--Warning--] Team HP lower than 25%. Aborting.")
                            self.loop.close()
                            self.loop.stop()
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
                    if (dergcount < 3):
                        print("[--Warning--] Less than 3 dergs in party. Rectify.")
                        os.system("pause")
                        self.loop.close()
                        os.system("pause")
                        self.loop.stop()
                        os.system("pause")
                    self.bId = msg['args'][0]['battleId']
                    go = {"name": "coliseum_battleLoaded",
                          "args": [{"battleId": self.bId, "user": Coliseum.userid}]}
                    goforth = "5:::" + json.dumps(go, separators=(',', ':'))
                    self.loop.call_later(random.uniform(self.mindelay, self.maxdelay), self.sendMessage, goforth.encode('utf-8'))
                    # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay) + 0.01, print, "-> {}".format(goforth))
                    # with open(Coliseum.userid + '.log', 'a') as p:
                    #     p.write("-> {}".format(goforth) + '\n')
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
                        # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay) + 0.01, print, "-> {}".format(goforth))
                        # with open(Coliseum.userid + '.log', 'a') as p:
                        #     p.write("-> {}".format(goforth) + '\n')
                elif (msg['name'] == 'finalizeAbility'):
                    self.fa = msg
                    if not self.fa['args'][0]['newTurns'] == 0:
                        if not re.search('^e\d+x+', str(self.fa['args'][0]['newTurns']['array'][0]['id'])):
                            if self.enemyList:
                                # for d in self.fa['args'][0]['newTurns']['array']:
                                #     if ((float(d['health']) < float((d['maxHP'])*0.25)) and d['team'] == 1):
                                #         self.loop.close()
                                #         self.loop.stop()
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
                                # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay) + 0.01, print, "-> {}".format(goforth))
                                # with open(Coliseum.userid + '.log', 'a') as p:
                                #     p.write("-> {}".format(goforth) + '\n')
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
                                        self.warning = 0
                                        self.loop.close()
                                        self.loop.stop()
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

                    if self.config['account']['coliseum']['trainingmode'] == 'true':
                        print("[Level]", str(self.fb['args'][0]['playerSet'][int(self.config['account']['coliseum']['trainingpos'])]['level']),
                              " [Exp]", str(self.fb['args'][0]['playerSet'][int(self.config['account']['coliseum']['trainingpos'])]['xp_now']))
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
                    # self.loop.call_later(random.uniform(self.mindelay, self.maxdelay) + 0.01, print, "-> {}".format(goforth))
                    # with open(Coliseum.userid + '.log', 'a') as p:
                    #     p.write("-> {}".format(goforth) + '\n')
        except KeyboardInterrupt:
            sys.exit()

    def onClose(self, wasClean, code, reason):
        print('[' + str(datetime.datetime.now().time())[:-3] + '] ' + "WebSocket connection closed: {0}".format(reason))
        # self.loop.close()
        self.loop.stop()
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
        elemult = getElementalMultipler(attacker, defender)
        return (elemult * ((4 * attacker['strength'] + 75) - (math.floor(defender['defense'] / 3.) * 4 + (defender['defense'] % 3))))

    def getElementalMultipler(attacker, defender):
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
        elemult = getElementalMultipler(self, attacker, defender)
        return (elemult * ((4 * attacker['intellect'] + 75) - (math.floor(defender['mind'] / 3.) * 4 + (defender['mind'] % 3))))

    def getElementalUltimate(self, attacker, defender):
        elemult = getElementalMultipler(attacker, defender)
        return (elemult * (6 * attacker['intellect'] + 17) - (2 * defender['mind']))

    def getEnvenomDOT(self, attacker, defender):
        # check
        return ((attacker['intellect'] * 10 + 20) / 5.)

    def getEnfeeble(self, attacker, defender):
        elemult = getElementalMultipler(attacker, defender)
        return (elemult * ((2 * attacker['intellect'] + 100) - math.floor(defender['mind'] / 3.) * 2 + math.round((defender['mind'] % 3) / 3.)))
