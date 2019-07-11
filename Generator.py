import csv
import random
import os

ALL_SORTED_LINEUPS = []


# Get players from csv file
def get_players():

    # Open csv file and save each row to player_list
    path = os.path.join(os.path.expanduser(
        '~'), 'Documents', 'FanDuel1125.csv')
    dfs_file_obj = open(path, 'r')
    dfs_reader = csv.reader(dfs_file_obj)
    player_list = []

    for row in dfs_reader:
        player_list.append(row)
    dfs_file_obj.close()

    # Define keys for player dictionaries in keys_list
    keys_list = ['ID', 'position', 'name', 'price', 'team']

    # Make a list of dictionaries of each player
    player_dict_list = [dict(zip(keys_list, player)) for player in player_list]

    player_select(player_dict_list)


# Get player selection from user
def player_select(player_dict_list):

    # Put the name of all players in player_name_list
    player_name_list = [player['name'] for player in player_dict_list]

    # Ask for player name input, find it in player_name_list, add player dictionary to sel_list
    # If name isn't in player_name_list, get another name
    # If input is 'DONE', break out of loop
    sel_list = []
    while True:
        player_sel = input(
            'Type in the name of a player or type done to finish: ').upper()
        if player_sel != 'DONE':
            if player_sel in player_name_list:
                for row in player_dict_list:
                    if row['name'] == player_sel:
                        sel_list.append(row)
                        break
            else:
                print(f'I did not find {player_sel}')
        else:
            break

    # Ask how many lineups to generate and set the value to num_lineups_int
    while True:
        try:
            num_lineups = int(input('How many lineups do you want to generate? '))
            break
        except ValueError:
            print("Enter an integer.")

    # Create final_lineup_list that generates x number of lineups
    final_lineup_list = generate_lineup(sel_list, num_lineups)

    # Pass final_lineup_list to writeCSV to generate CSV file of all lineups
    write_csv(final_lineup_list)


# Generate correct number of lineups
def generate_lineup(sel_list, num_lineups):

    # Create each positions list
    qb_list = get_position_list(sel_list, 'QB')
    rb_list = get_position_list(sel_list, 'RB')
    wr_list = get_position_list(sel_list, 'WR')
    te_list = get_position_list(sel_list, 'TE')
    def_list = get_position_list(sel_list, 'D')

    # Combine rb and wr lists to get flex list
    combined_rb_wr_list = rb_list + wr_list
    return_list = []

    # Generate lineups until return_list has correct number of lineups
    while len(return_list) < num_lineups:

        # Create lineup_dict_list to hold players selected at each position
        lineup_dict_list = []

        # Add a random qb from qb_list to lineup_dict_list
        lineup_dict_list += random.sample(qb_list, 1)

        # Add 2 random rbs from rb_list to lineup_dict_list
        lineup_dict_list += random.sample(rb_list, 2)

        # Add 3 random wrs to lineup_dict_list
        lineup_dict_list += random.sample(wr_list, 3)

        # Add a random te to lineup_dict_list
        lineup_dict_list += random.sample(te_list, 1)

        # Create flex_list that includes all rbs and wrs except those already selected
        # Add a random flex to lineup_dict_list
        flex_list = [
            player for player in combined_rb_wr_list if player not in lineup_dict_list]
        lineup_dict_list += random.sample(flex_list, 1)

        # Add a random def to lineup_dict_list
        lineup_dict_list += random.sample(def_list, 1)

        # Check price of lineup is <=60000 and >59000 and is not a duplicate and does not have
        # more than 4 players from the same team
        # If True return lineup to be added to final_lineup_list, else generate a new lineup
        if check_price(lineup_dict_list) and check_duplicate(lineup_dict_list) and check_teams(lineup_dict_list):
            return_list.append(lineup_dict_list)

    return return_list


# Return a list of players at specified position
def get_position_list(sel_list, position):

    return [s for s in sel_list if s['position'] == position]


# Check price is between 59000 and 60000
def check_price(lineup_dict_list):

    # Get price of each player in lineup and subtract it from salary
    salary = sum([int(i['price']) for i in lineup_dict_list])

    # Return true if salary is still >= 0 but < 1000, else return false
    return 59000 <= salary <= 60000


# Check that the lineup hasn't been used already
def check_duplicate(lineup_dict_list):

    # get global all_lineups to compare lineup_dict_list to
    global ALL_SORTED_LINEUPS

    # Sort players in lineup by name and check if it's in ALL_SORTED_LINEUPS
    # If not return true and add sorted_lineup to global ALL_SORTED_LINEUPS, else return false
    sorted_lineup = sorted(lineup_dict_list, key=lambda player: player['name'])
    if sorted_lineup not in ALL_SORTED_LINEUPS:
        ALL_SORTED_LINEUPS.append(sorted_lineup)
        return True
    else:
        return False


# Check that no team has more than 4 players in lineup
def check_teams(lineup_dict_list):

    team_list = [player['team'] for player in lineup_dict_list]
    team_set = list(set(team_list))
    for i in range(len(team_set)):
        if team_list.count(team_set[i]) >= 4:
            return False
    return True


# Write a csv file containing all the lineups generated
def write_csv(final_lineup_list):

    # Add the ID of each player on a team to a team list, then add all team lists to id_list
    id_list = []
    for team in final_lineup_list:
        team_list = []
        for player in team:
            team_list.append(player['ID'])
        id_list.append(team_list)

    # Write id_list to csv file
    path = os.path.join(os.path.expanduser(
        '~'), 'Documents', 'FanDuel1125lineups.csv')
    my_file = open(path, 'w', newline='')
    with my_file:
        writer = csv.writer(my_file)
        writer.writerows(id_list)


get_players()
