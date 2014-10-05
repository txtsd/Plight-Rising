#!/usr/bin/env python3
# ---------------------------------------------------------------------
# ------------------------- Plight Rising -----------------------------
# -----------------------------txtsd-----------------------------------
# ---------------------------------------------------------------------

"""Runs the bot"""

# Imports -------------------------------------------------------------
import os
import sys
import time
import random
import datetime
from pytz import timezone
from configobj import ConfigObj
from classes.FRAccount import FRAccount
from classes.Familiar import Familiar
from classes.Gather import Gather
from classes.Coliseum import Coliseum
# End Imports ---------------------------------------------------------

config = ConfigObj('config.ini')

if config['account']['username'] or (not config['account']['username'] == 'herp' and config['account']['password'] == 'derp'):
    fruser = config['account']['username']
    frpass = config['account']['password']
    proxyaddress = config['account']['proxy']
    gather = False
    bond = False
    coli = True
    start = datetime.time(23, 58)
    end = datetime.time(0, 32)
    pst = timezone('US/Pacific')

    acc = FRAccount(fruser, frpass, proxyaddress)
    if not (start < datetime.datetime.now(tz=pst).time() or datetime.datetime.now(tz=pst).time() < end):
        if acc.login():
            gHandler = Gather(acc)
            fHandler = Familiar(acc)
            if gather:
                gHandler.gather()
            if bond:
                fHandler.bond()
            if coli:
                try:
                    cHandler = None
                    cHandler = Coliseum()
                    cHandler.play(acc)
                except Exception as e:
                    # pass
                    # e = sys.exc_info()[0]
                    print("clientderp")
                    print(type(e))
                    print(e.args)
                    print(e)
                # finally:
                #     # del cHandler
                #     time.sleep(random.randint(1, 2))
                #     # acc.login()
    else:
        if os.path.isfile(fruser + '.bin'):
            os.remove(fruser + '.bin')
        time.sleep(10)
else:
    print('Please set up your username and password, among other things, in config.ini')
    sys.exit()
