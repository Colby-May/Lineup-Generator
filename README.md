# Lineup-Generator
Generate FanDuel football lineups


import csv
import random
from operator import itemgetter
all_lineups = []

def getPlayers():

    # Open csv file and save each row as a list player_list
    dfsFileObj = open("C:\\Users\\Colby\\Python\\Fanduel1202.csv", 'r')
    dfsReader = csv.reader(dfsFileObj)
    player_list = []

    for row in dfsReader:
        player_list.append(row)
    dfsFileObj.close()

    # Define keys for player dictionary
    desc_keys = ['ID', 'position', 'name', 'price']

    # Make a list (player_dict_list) of player dictionaries
    player_dict_list = []
    for x in player_list:
        player_dict_list += [{desc_keys[i] : x[i] for i in range(len(x))}]

    playerSelect(player_dict_list)

def playerSelect(player_dict_list):

    qb_list = []
    rb_list = []
    wr_list = []
    te_list = []
    def_list = []
    player_name_list = []
    final_lineup_list = []

    # Make a list of all player names
    for line in player_dict_list:
        player_name_list.append(line['name'])

    # Ask for player name, find it in player_name_list, add player dictionary to appropriate position list
    # If name isn't in player_name_list, get another name
    # If input is 'Done', break out of loop
    while True:
        player_sel = input('Select a player or type done: ').title()
        if player_sel != 'Done':
            if player_sel in player_name_list:
                for row in player_dict_list:
                    if player_sel in row.values():
                        if 'QB' in row.values():
                            qb_list.append(row)
                        elif 'RB' in row.values():
                            rb_list.append(row)
                        elif 'WR' in row.values():
                            wr_list.append(row)
                        elif 'TE' in row.values():
                            te_list.append(row)
                        else:
                            def_list.append(row)
            else:
                print('I didn\'t find that player.')
        else:
            break

    # Ask how many lineups to generate and set the value to num_lineups
    num_lineups = int(input('How many lineups do you want to generate? '))

    # Call generateLineup x times, each time appending the returned list to final_lineup_list
    for x in range(num_lineups):
        final_lineup_list.append(generateLineup(qb_list,rb_list, wr_list, te_list, def_list))

    writeCSV(final_lineup_list)

def generateLineup(qb_list,rb_list, wr_list, te_list, def_list):

    lineup_dict_list = []
    # Combine rb and wr lists to get full flex list
    combined_list = rb_list + wr_list
    
    # Add a random qb to lineup_dict_list
    lineup_dict_list += random.sample(qb_list, 1)

    # Add 2 random rbs to lineup_dict_list
    # Get selections to remove from flex list later
    rb_selections = random.sample(rb_list, 2)
    lineup_dict_list += rb_selections

    # Add 3 random wrs to lineup_dict_list
    # Get selections to remove from flex list later
    wr_selections = random.sample(wr_list, 3)
    lineup_dict_list += wr_selections

    # Add a random te to lineup_dict_list
    lineup_dict_list += random.sample(te_list, 1)


    #Add selected rbs and wrs to remove_list
    #create flex_list that includes all rbs and wrs except those in remove_list
    # Add a random flex to lineup_dict_list
    remove_list = rb_selections + wr_selections
    flex_list = [x for x in combined_list if x not in remove_list]
    lineup_dict_list += random.sample(flex_list, 1)

    # Add a random def to lineup_dict_list
    lineup_dict_list += random.sample(def_list, 1)

    # Check price of lineup is <=60000 and is not a duplicate
    # If True return lineup, else get a new lineup
    if checkPrice(lineup_dict_list) and checkDuplicate(lineup_dict_list):
        return lineup_dict_list
    else:
        generateLineup(qb_list,rb_list, wr_list, te_list, def_list)


def checkPrice(lineup_dict_list):

    # Get price of each player in lineup and subtract it from salary
    salary = 60000
    for player in lineup_dict_list:
        salary -= int(player['price'])

    # Return true if salary is still >= 0 but < 1000, else return false
    if salary >= 0 and salary < 1000:
        return True
    else:
        return False

def checkDuplicate(lineup_dict_list):
    global all_lineups

    # Sort players in lineup by name and check if it's in all_lineups
    # If not return true, else return false
    sorted_lineup = sorted(lineup_dict_list, key=itemgetter('name'))
    if sorted_lineup not in all_lineups:
        all_lineups.append(sorted_lineup)
        return True
    else:
        return False

def writeCSV(final_lineup_list):

    id_list = []

    # Add the ID of each player on a team to a team list, then add all team lists to id_list
    for team in final_lineup_list:
        team_list = []
        for player in team:
            team_list.append(player['ID'])
        id_list.append(team_list)

    # Write id_list to csv file
    myFile = open('C:\\Users\\Colby\\Python\\Fanduel1202Lineup.csv', 'w', newline='')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(id_list)

getPlayers()
