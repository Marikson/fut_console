import display
import vars
import request_try
import list_players


def my_team():
    stay = True
    while stay:
        display.my_team_menupoints()
        choice = input("  Enter number of menupoint: ")
        try:
            if choice == "back":
                display.print_info("  Going back to FUT MENU")
                return
            elif int(choice) == 1:
                list_players.list_starting_11()
            elif int(choice) == 2:
                list_players.list_owned_players()
            elif int(choice) == 3:
                edit_team()
            else:
                warning_string = "  No menu point found with number: " + choice + "."
                display.print_warning(warning_string)
        except ValueError:
            warning_string = "  Aspect input must be a number! Given '" + choice + "' is wrong."
            display.print_warning(warning_string)


def edit_team():
    stay = True
    while stay:
        list_players.list_owned_players()
        list_players.list_starting_11()

        input_names = input("Enter the full name of players you want to change: ")
        if input_names == "back":
            display.print_info("Going back to TEAM EDITOR")
            return

        players_to_sub = input_names.split(',')
        for i in range(len(players_to_sub)):
            players_to_sub[i] = players_to_sub[i].rstrip().lstrip()
            if players_to_sub[i] == "back":
                display.print_info("Going back to TEAM EDITOR")
                return
        while "" in players_to_sub:
            players_to_sub.remove("")

        if len(players_to_sub) > 2 or len(players_to_sub) <= 1:
            display.print_warning("Changing requires 2 players separated with ','!")
        else:
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

    if starting_found + owned_found == 2:
        if len(at_starting) > len(at_owned):
            if len(at_starting) < 2:
                display.print_warning("No change.")
                return False
            else:
                starting_ind = list(at_starting.keys())
                starting[starting_ind[0]] = at_starting[starting_ind[1]]
                starting[starting_ind[1]] = at_starting[starting_ind[0]]
                patched = request_try.try_request_patch(vars.users_id_url, {'starting_11': starting})
                if patched:
                    display.print_info_green("Players switched successfully!")
                    return True
                else:
                    display.print_warning("Switch failed.")
                    return False

        elif len(at_starting) < len(at_owned):
            # Pointless, non visible change
            display.print_warning("You are trying to switch two players from substitutes, which is pointless.")
            return False
        else:
            owned_ind = list(at_owned.keys())
            starting_ind = list(at_starting.keys())
            owned[int(owned_ind[0])] = at_starting[starting_ind[0]]
            starting[starting_ind[0]] = at_owned[owned_ind[0]]
            patch_starting = request_try.try_request_patch(vars.users_id_url, {'starting_11': starting})
            patch_owned = request_try.try_request_patch(vars.users_id_url, {'owned_players': owned})
            if patch_owned and patch_starting:
                display.print_info_green("Players switched successfully!")
                return True
            else:
                display.print_warning("Switch failed.")
                return False

    else:
        display.print_warning("One, or more of the names are misspelled!")
        return False
