# Lineup-Generator
# Generate FanDuel football lineups


import csv
import random
from operator import itemgetter
all_sorted_lineups = []

def getPlayers():

    # Open csv file and save each row to player_list
    dfsFileObj = open("C:\\Users\\Colby\\Python\\Fanduel1202.csv", 'r')
    dfsReader = csv.reader(dfsFileObj)
    player_list = []

    for row in dfsReader:
        player_list.append(row)
    dfsFileObj.close()

    # Define keys for player dictionaries in keys_list
    keys_list = ['ID', 'position', 'name', 'price']

    # Make dictionaries for each player and add them to player_dict_list
    player_dict_list = []
    for x in player_list:
        player_dict_list += [{desc_keys[i] : x[i] for i in range(len(x))}]

    playerSelect(player_dict_list)

def playerSelect(player_dict_list):

    # Put the name of all players in player_name_list
    player_name_list = []
    for player in player_dict_list:
        player_name_list.append(player['name'])

    # Create list for each position
    # Ask for player name input, find it in player_name_list, add player dictionary to appropriate position list
    # If name isn't in player_name_list, get another name
    # If input is 'Done', break out of loop
    qb_list = []
    rb_list = []
    wr_list = []
    te_list = []
    def_list = []
    while True:
        player_sel = input('Type in the name of a player or type done to finish: ').title()
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
                print('I did not find ' + player_sel)
        else:
            break

    # Ask how many lineups to generate and set the value to num_lineups_int
    num_lineups_int = int(input('How many lineups do you want to generate? '))

    # Call generateLineup num_lineups_int times, each time appending the returned list to final_lineup_list
    # Pass all position lists to generateLineup
    final_lineup_list = []
    for x in range(num_lineups_int):
        final_lineup_list.append(generateLineup(qb_list,rb_list, wr_list, te_list, def_list))
    
    # Pass final_lineup_list to writeCSV to generate CSV file of all lineups
    writeCSV(final_lineup_list)

def generateLineup(qb_list,rb_list, wr_list, te_list, def_list):
    
    # Create lineup_dict_list to hold players selected at each position
    lineup_dict_list = []
    
    # Combine rb and wr lists to get flex list
    combined_rb_wr_list = rb_list + wr_list
    
    # Add a random qb from qb_list to lineup_dict_list
    lineup_dict_list += random.sample(qb_list, 1)

    # Add 2 random rbs from rb_list to lineup_dict_list
    # Get RB selections to remove from flex list later
    rb_selections = random.sample(rb_list, 2)
    lineup_dict_list += rb_selections

    # Add 3 random wrs to lineup_dict_list
    # Get WR selections to remove from flex list later
    wr_selections = random.sample(wr_list, 3)
    lineup_dict_list += wr_selections

    # Add a random te to lineup_dict_list
    lineup_dict_list += random.sample(te_list, 1)


    # Add previously selected rbs and wrs to remove_list
    # Create flex_list that includes all rbs and wrs except those in remove_list
    # Add a random flex to lineup_dict_list
    remove_list = rb_selections + wr_selections
    flex_list = [player for player in combined_rb_wr_list if player not in remove_list]
    lineup_dict_list += random.sample(flex_list, 1)

    # Add a random def to lineup_dict_list
    lineup_dict_list += random.sample(def_list, 1)

    # Check price of lineup is <=60000 and >59000 and is not a duplicate
    # If True return lineup to be appended to final_lineup_list, else generate a new lineup
    if checkPrice(lineup_dict_list) and checkDuplicate(lineup_dict_list):
        return lineup_dict_list
    else:
        generateLineup(qb_list, rb_list, wr_list, te_list, def_list)


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

    # get global all_lineups to compare lineup_dict_list to
    global all_sorted_lineups

    # Sort players in lineup by name and check if it's in all_sorted_lineups
    # If not return true and add sorted_lineup to global all_sorted_lineups, else return false
    sorted_lineup = sorted(lineup_dict_list, key=itemgetter('name'))
    if sorted_lineup not in all_lineups:
        all_sorted_lineups.append(sorted_lineup)
        return True
    else:
        return False

def writeCSV(final_lineup_list):

    # Add the ID of each player on a team to a team list, then add all team lists to id_list
    id_list = []
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
