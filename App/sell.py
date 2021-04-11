import display
import login
import vars
import request_try
import list_players


def sell_player():
    list_players.list_owned_players()
    name_to_sell = input("Enter the full name of player you want to sell: ")
    if name_to_sell == "back":
        print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
        display.get_menu_choice()
    name_to_sell = name_to_sell.rstrip().lstrip()
    players_with_name_to_sell = request_try.try_request_get(vars.players_URL, {'player_extended_name': name_to_sell})

    players_futbin_id = []
    players_resource_id = []
    for i in range(len(players_with_name_to_sell)):
        players_futbin_id.append(int(players_with_name_to_sell[i]['futbin_id']))
        players_resource_id.append(int(players_with_name_to_sell[i]['resource_id']))

    matched = list_players.select_matching(players_futbin_id, "owned_players")
    if matched:
        owned = matched.ids
        at_owned = matched.at_ind
        owned.remove(at_owned)
    else:
        print(display.Bcolors.WARNING + "The name is probably misspelled!" + display.Bcolors.ENDC)

