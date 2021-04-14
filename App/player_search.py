import display
import vars
import request_try


def search_for_player():
    stay = True
    while stay:
        display.player_search_menupoints()
        input_nums = input("  Enter aspect(s)(separated by space) you want to filter by: ")
        nums_list = input_nums.split()
        can_stay = stay_check(nums_list)
        if can_stay:
            just_nums = is_valid_input(nums_list)
            if just_nums:
                params = get_aspects(nums_list)
                if params:
                    matched_players = request_try.try_request_get(vars.players_URL, params)
                    if matched_players:
                        display.show_players(matched_players)
                        names = input("      Enter the full name of found player/s to get more details: ")
                        if names == "back":
                            print(display.Bcolors.OKBLUE + "      Going back to PLAYER SEARCH" + display.Bcolors.ENDC + '\n')
                        else:
                            more_details(names)
                    else:
                        print(display.Bcolors.OKCYAN + "No matching player with params above!" + display.Bcolors.ENDC + '\n')
                else:
                    print(display.Bcolors.OKBLUE + "      Going back to PLAYER SEARCH" + display.Bcolors.ENDC + '\n')
        else:
            stay = False
    return


def stay_check(inp_nums):
    for i in range(len(inp_nums)):
        if inp_nums[i] == "back":
            print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
            return False
    return True


def is_valid_input(inp_nums):
    for i in range(len(inp_nums)):
        try:
            if int(inp_nums[i]) > 8 or int(inp_nums[i]) < 1:
                print(display.Bcolors.WARNING + "  No aspect found with number: " + inp_nums[i] + "!" + display.Bcolors.ENDC)
                return False

        except ValueError:
            print(display.Bcolors.WARNING + "  Aspect input must be a number! Given '" + inp_nums[i] + "' is wrong." + display.Bcolors.ENDC)
            return False
    return True


def get_aspects(nums_list):
    params = {}
    for i in range(len(nums_list)):
        given_val = input("      Enter " + vars.search_aspect[int(nums_list[i]) - 1] + ": ")
        if given_val == 'back':
            return False
        else:
            params[vars.search_aspect[int(nums_list[i]) - 1]] = given_val
    return params


def more_details(player_names):
    players_to_request = player_names.split(',')
    for i in range(len(players_to_request)):
        players_to_request[i] = players_to_request[i].rstrip().lstrip()
        if players_to_request[i] == "back":
            print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
            return
    while "" in players_to_request:
        players_to_request.remove("")

    players_with_details = request_try.try_request_get(vars.players_URL, {'player_extended_name': players_to_request})
    if players_with_details:
        display.show_extended_players(players_with_details)
    else:
        print(display.Bcolors.OKCYAN + "No matching player with params above!" + display.Bcolors.ENDC + '\n')

