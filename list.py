#!/usr/bin/env python3
# ---------------------------------------------------------------------
# ------------------------- Plight Rising -----------------------------
# -----------------------------txtsd-----------------------------------
# ---------------------------------------------------------------------

"""Lists things"""

# Imports -------------------------------------------------------------
import os
import json
# End Imports ---------------------------------------------------------

userID = ''
derp = []
things = []
venue = ''
# training_fields, woodland_border, scorched_forest, sandswept_delta, forgotten_cave,
# bamboo_waterfall, waterway, arena, boreal_wood, harpys_roost, mire, kelp_beds
time = 0
enemies = {}
total = 0
noloot = 0
dec = json.JSONDecoder()


with open(userID + '.txt', 'r') as f:
    try:
        herp = f.read()
    except:
        print("--Done Reading--")

for x in herp.split('\n'):
    try:
        derp.append(dec.decode(x))
    except:
        print("--Done Parsing--")

print(str(len(derp)) + ' entries')

for x in derp:
    if (x['venue'] == venue) and (x['time'] > time):
        total += 1
        if x['loot']:
            for y in x['loot']:
                if y not in things:
                    things.append(y)
        else:
            noloot += 1
        temp = ''
        for y in x['enemies']:
            temp += (y['name'] + ' | ')
        if temp not in enemies:
            enemies[temp] = 0
        enemies[temp] += 1

print("Battles: " + str(total), "Noloot: " + str(noloot))
things.sort(key=lambda herp: (herp['subtype'], herp['name']))

print('')
for x in enemies:
    print(x, str(enemies[x]/total*100)[:7] + '%')
print('')

for i, w in enumerate(things):
    instances = 0
    count = 0
    prob = {'1': 0, '2': 0, '3': 0, '4': 0}
    for x in derp:
        if (x['venue'] == venue) and (x['time'] > time):
            if x['loot']:
                num = 0
                for y in x['loot']:
                    if y['name'] == w['name']:
                        num += 1
                        count += 1
                if not num == 0:
                    prob[str(num)] += 1
    print(w['subtype'], str(count / total * 100.0)[:7] + '%', w['name'].replace('\u2019', "'") + ": " + str(count))
os.system("pause")
