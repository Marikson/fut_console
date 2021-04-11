import display
import login
import vars
import request_try
import list_players


def my_team():
    display.my_team_menupoints()
    choice = input("  Enter number of menupoint: ")
    if choice == "back":
        print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
        display.get_menu_choice()
    elif int(choice) == 1:
        list_players.list_starting_11()
        # list_players('starting_11', True)
    elif int(choice) == 2:
        list_players.list_owned_players()
        # list_players('owned_players', True)
    elif int(choice) == 3:
        edit_starting_eleven()
    else:
        print(display.Bcolors.WARNING + "  No menupoint found with number: " + choice + "!" + display.Bcolors.ENDC)
        my_team()

"""
def list_players(type_of_players, can_return):
    users_players = get_users_players_id(type_of_players)
    users_players_extended_list = []
    positions = None
    if type(users_players) is dict:
        positions = list(users_players.keys())
        users_players = list(users_players.values())

    players = request_try.try_request_get(vars.players_URL, {'futbin_id': users_players})

    for i in range(len(players)):
        users_players_extended_list.append(players[i])

    print(display.Bcolors.OKBLUE + "Your " + type_of_players.replace('_', ' ') + display.Bcolors.ENDC)
    if type_of_players == "starting_11":
        display.show_starting_11(users_players_extended_list, positions)
    else:
        display.show_players(users_players_extended_list)
    if can_return:
        my_team()
"""

def edit_starting_eleven():
    # list_players('owned_players', False)
    # list_players('starting_11', False)
    list_players.list_owned_players()
    list_players.list_starting_11()

    input_names = input("Enter the full name of players you want to change: ")
    if input_names == "back":
        print(display.Bcolors.OKBLUE + "  Going back to TEAM EDITOR" + display.Bcolors.ENDC + '\n')
        my_team()

    players_to_sub = input_names.split(',')
    for i in range(len(players_to_sub)):
        players_to_sub[i] = players_to_sub[i].rstrip().lstrip()
        if players_to_sub[i] == "back":
            print(display.Bcolors.OKBLUE + "  Going back to TEAM EDITOR" + display.Bcolors.ENDC + '\n')
            my_team()
    while "" in players_to_sub:
        players_to_sub.remove("")

    if len(players_to_sub) > 2 or len(players_to_sub) <= 1:
        print(display.Bcolors.WARNING + "Changing requires 2 players separated with ','!" + display.Bcolors.ENDC + '\n')
        edit_starting_eleven()

    players = request_try.try_request_get(vars.players_URL, {'player_extended_name': players_to_sub})
    players_futbin_id = []
    for i in range(len(players)):
        players_futbin_id.append(int(players[i]['futbin_id']))

    changing(players_futbin_id)


def changing(futbin_ids):
    matched_starting = list_players.select_matching(futbin_ids, "starting_11")
    starting = matched_starting.ids
    at_starting = matched_starting.at_ind
    starting_found = matched_starting.found_counter

    matched_owned = list_players.select_matching(futbin_ids, "owned_players")
    owned = matched_owned.ids
    at_owned = matched_owned.at_ind
    owned_found = matched_owned.found_counter

    users_id_url = vars.users_URL + '/' + str(login.user_id)
    if starting_found + owned_found == 2:
        if len(at_starting) > len(at_owned):
            starting_ind = list(at_starting.keys())
            starting[starting_ind[0]] = at_starting[starting_ind[1]]
            starting[starting_ind[1]] = at_starting[starting_ind[0]]
            post = request_try.try_request_post(users_id_url, {'starting_11': starting})
            if post:
                print(display.Bcolors.OKGREEN + "Players switched successfully!" + display.Bcolors.ENDC)

        elif len(at_starting) < len(at_owned):
            # Pointless, non visible change
            """
            owned_ind = list(at_owned.keys())
            owned[int(owned_ind[0])] = at_owned[owned_ind[1]]
            owned[int(owned_ind[1])] = at_owned[owned_ind[0]]
            post = request_try.try_request_post(users_id_url, {'owned_players': owned})
            if post:
                print(display.Bcolors.OKGREEN + "Players changed successfully!" + display.Bcolors.ENDC)
            else:
                print(display.Bcolors.WARNING + "Change failed!" + display.Bcolors.ENDC)
            """
            print(display.Bcolors.WARNING + "You are trying to change two players form subsitutes, which is pointless!" + display.Bcolors.ENDC)
        else:
            owned_ind = list(at_owned.keys())
            starting_ind = list(at_starting.keys())
            owned[int(owned_ind[0])] = at_starting[starting_ind[0]]
            starting[starting_ind[0]] = at_owned[owned_ind[0]]
            post_starting = request_try.try_request_post(users_id_url, {'starting_11': starting})
            post_owned = request_try.try_request_post(users_id_url, {'owned_players': owned})
            if post_owned and post_starting:
                print(display.Bcolors.OKGREEN + "Players switched successfully!" + display.Bcolors.ENDC)
            else:
                print(display.Bcolors.WARNING + "Change failed!" + display.Bcolors.ENDC)

    else:
        print(display.Bcolors.WARNING + "One, or more of the names is/are misspelled!" + display.Bcolors.ENDC)

    edit_starting_eleven()

# Nathan Aké, Allan Saint-Maximin
# Nathan Aké, Harry Kite
