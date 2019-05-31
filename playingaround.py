import random
from collections import Counter


def getPositionList(players, position):
    return [p for p in players if p['position'] == position]


players = [{
    'name': 'Baker Mayfield',
    'position': 'QB',
    'price': 7000,
    'team': 'CLE'
}, {
    'name': 'Nick Chubb',
    'position': 'RB',
    'price': 6200,
    'team': 'CLE'
}, {
    'name': 'Jarvis Landry',
    'position': 'WR',
    'price': 5800,
    'team': 'CLE'
}, {
    'name': 'David Njoku',
    'position': 'TE',
    'price': 5400,
    'team': 'CLE'
}, {
    'name': 'Cleveland Browns',
    'position': 'DEF',
    'price': 4000,
    'team': 'CLE'
}, {
    'name': 'Tom Brady',
    'position': 'QB',
    'price': 8000,
    'team': 'NE'
}, {
    'name': 'Julian Edelman',
    'position': 'WR',
    'price': 6800,
    'team': 'NE'
}, {
    'name': 'James White',
    'position': 'RB',
    'price': 6000,
    'team': 'NE'
}, {
    'name': 'Rob Gronkowski',
    'position': 'TE',
    'price': 7200,
    'team': 'NE'
},
           {
               'name': 'New England Patriots',
               'position': 'DEF',
               'price': 3800,
               'team': 'NE'
           },
           {
               'name': 'Jared Goff',
               'position': 'QB',
               'price': 8200,
               'team': 'LAR'
           },
           {
               'name': 'Todd Gurley',
               'position': 'RB',
               'price': 8400,
               'team': 'LAR'
           },
           {
               'name': 'Cooper Kupp',
               'position': 'WR',
               'price': 7000,
               'team': 'LAR'
           },
           {
               'name': 'Lance Kendricks',
               'position': 'TE',
               'price': 3200,
               'team': 'LAR'
           },
           {
               'name': 'Los Angeles Rams',
               'position': 'DEF',
               'price': 4000,
               'team': 'LAR'
           }]

qbs = getPositionList(players, 'QB')
rbs = getPositionList(players, 'RB')
wrs = getPositionList(players, 'WR')
tes = getPositionList(players, 'TE')
defense = getPositionList(players, 'DEF')
rb_wr_comb = rbs + wrs

team = [
    random.choice(qbs), (*random.sample(rbs, 2)), (*random.sample(wrs, 3)),
    random.choice(tes),
    random.choice(defense)
]

flex = [f for f in rb_wr_comb if f['name'] not in [t['name'] for t in team]]

team.insert(7, random.choice(flex))

price = 0

teams_used = [t['team'] for t in team]
teams_used_set = list({t['team'] for t in team})

for i in range(len(teams_used_set)):
    print(teams_used.count(teams_used_set[i]))
