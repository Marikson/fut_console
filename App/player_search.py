import display
import vars
import request_try

def search_for_player():
    display.player_search_menupoints()
    params = {}
    input_nums = input("  Enter aspect(s)(separated by space) you want to filter by: ")
    nums_list = input_nums.split()
    for i in range(len(nums_list)):
        try:
            if nums_list[i] == "back":
                print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
                display.get_menu_choice()
            elif int(nums_list[i]) > 8 or int(nums_list[i]) < 1:
                print(display.Bcolors.WARNING + "  No aspect found with number: " + nums_list[i] + "!" + display.Bcolors.ENDC)
                search_for_player()

        except ValueError:
            print(display.Bcolors.WARNING + "  Aspect input must be a number! Given '" + nums_list[i] + "' is wrong." + display.Bcolors.ENDC)
            search_for_player()

    for i in range(len(nums_list)):
        given_val = input("      Enter " + vars.search_aspect[int(nums_list[i]) - 1] + ": ")
        if given_val == 'back':
            search_for_player()
        else:
            params[ vars.search_aspect[int(nums_list[i]) - 1]] = given_val

    matched_players = request_try.try_request_get(vars.players_URL, params)
    if matched_players:
        display.show_players(matched_players)
        names = input("      Enter the full name of found player/s to get more details: ")
        if names == "back":
            print(display.Bcolors.OKBLUE + "  Going back to PLAYER SEARCH" + display.Bcolors.ENDC + '\n')
            search_for_player()
        else:
            more_details(names)
    else:
        print(display.Bcolors.OKCYAN + "No matching player with params above!" + display.Bcolors.ENDC + '\n')





def more_details(player_names):
    players_to_request = player_names.split(',')
    for i in range(len(players_to_request)):
        players_to_request[i] = players_to_request[i].rstrip().lstrip()
        if players_to_request[i] == "back":
            print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
            display.get_menu_choice()
    while "" in players_to_request:
        players_to_request.remove("")

    players_with_details = request_try.try_request_get(vars.players_URL, {'player_extended_name': players_to_request})
    if players_with_details:
        display.show_extended_players(players_with_details)
    else:
        print(display.Bcolors.OKCYAN + "No matching player with params above!" + display.Bcolors.ENDC + '\n')

    search_for_player()