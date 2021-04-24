import display
import vars
import request_try
import buy


def search_for_player(buy_purpose = False):
    stay = True
    while stay:
        if buy_purpose:
            coins = str(buy.get_coins())
            print(display.Bcolors.OKCYAN + "Your coins: " + coins + display.Bcolors.ENDC)
            display.market_search_menupoints()
        else:
            display.player_search_menupoints()
        input_nums = input("  Enter number(s) of aspect(s) you want to filter by: ")
        nums_list = input_nums.split(',')
        can_stay = stay_check(nums_list)
        if can_stay:
            just_nums = is_valid_input(nums_list, buy_purpose)
            if just_nums:
                params = get_aspects(nums_list, buy_purpose)
                if params:
                    if buy_purpose:
                        min_price = None
                        max_price = None
                        if 'min_price' in params:
                            min_price = params['min_price']
                            del params['min_price']
                        if 'max_price' in params:
                            max_price = params['max_price']
                            del params['max_price']
                        buy.buy_player(params, min_price, max_price)
                    else:
                        matched_players = request_try.try_request_get(vars.players_URL, params)
                        if matched_players:
                            display.show_players(matched_players)
                            still_detailed = True
                            while still_detailed:
                                names = input("      Enter the full name of found player to get more details: ")
                                still_detailed = more_details(names)
                        else:
                            display.print_info_cyan("      No matching player with params above!")
        else:
            stay = False
    return


def stay_check(inp_nums):
    for i in range(len(inp_nums)):
        inp_nums[i] = inp_nums[i].rstrip().lstrip()
        if inp_nums[i] == "back":
            display.print_info("  Going back to FUT MENU")
            return False
    return True


def is_valid_input(inp_nums, buy_purpose = False):
    top = 8
    if buy_purpose:
        top = 10
    if len(inp_nums) == 0:
        display.print_warning("  No aspect given!")
        return False
    for i in range(len(inp_nums)):
        inp_nums[i] = inp_nums[i].rstrip().lstrip()
        try:
            if int(inp_nums[i]) > top or int(inp_nums[i]) < 1:
                warning_string = "  No aspect found with number: " + inp_nums[i] + "!"
                display.print_warning(warning_string)
                return False

        except ValueError:
            warning_string = "  Aspect input must be a number! Given '" + inp_nums[i] + "' is wrong."
            display.print_warning(warning_string)
            return False
    return True


def get_aspects(nums_list, buy_purpose = False):
    aspect_list = vars.search_aspect
    if buy_purpose:
        aspect_list = vars.market_aspect
    params = {}
    for i in range(len(nums_list)):
        nums_list[i] = nums_list[i].rstrip().lstrip()
        empty_input = True
        key = list(aspect_list[int(nums_list[i]) - 1].keys())
        values = list(aspect_list[int(nums_list[i]) - 1].values())
        while empty_input:
            given_val = input("      Enter " + values[0] + ": ")
            given_val = given_val.lstrip().rstrip()
            if given_val == 'back':
                if buy_purpose:
                    display.print_info("      Going back to MARKET SEARCH")
                else:
                    display.print_info("      Going back to PLAYER SEARCH")
                return False
            elif given_val != "":
                params[key[0]] = given_val
                empty_input = False
            else:
                display.print_warning("      Aspect input can not be empty!")
    return params


def more_details(player_names):
    if len(player_names) == 0:
        display.print_warning("      No aspect given!")
        return False
    players_to_request = player_names.split(',')
    for i in range(len(players_to_request)):
        players_to_request[i] = players_to_request[i].rstrip().lstrip()
        if players_to_request[i] == "back":
            display.print_info("      Going back to PLAYER SEARCH")
            return False
    while "" in players_to_request:
        players_to_request.remove("")

    players_with_details = request_try.try_request_get(vars.players_URL, {'player_extended_name': players_to_request})
    if players_with_details:
        display.show_extended_players(players_with_details)
        return True
    else:
        display.print_info_cyan("      No matching player with params above!")
        return True
