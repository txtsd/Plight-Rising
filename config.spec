[account]
username = string(max=50)
password = string(max=50)
proxy = string(max=15)
useragent = string(max=200)
DNT = boolean(default=False)
pinkerton = boolean(default=False)
feed = boolean(default=False)

    [[gather]]
    area = option('earth', 'plague', 'wind', 'water', 'lightning', 'ice', 'shadow', 'light', 'arcane', 'nature', 'fire', default='earth')
    action = option('hunt', 'fish', 'catch', 'forage', 'dig', 'scavenge', default='hunt')

    [[bond]]
    mindelay = float(1, 60, default=2.0)
    maxdelay = float(1, 60, default=4.0)

    [[coliseum]]
    area = option('training_fields', 'woodland_border', 'scorched_forest', 'sandswept_delta', 'forgotten_cave', 'bamboo_waterfall', 'waterway', 'arena', 'boreal_wood', 'harpys_roost', 'mire', 'kelp_beds', default='training_fields')
    mindelay = float(1, 60, default=2.0)
    maxdelay = float(1, 60, default=4.0)
    trainingmode = boolean(default=False)
    trainingpos = integer(0, 2, default=2)
    debuglog = boolean(default=False)
