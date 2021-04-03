import requests
import fut_display
import fut_login
import fut_vars


def my_team():
    print(29 * "-", "TEAM EDITOR", 29 * "-")
    print("  1. Show starting 11")
    print("  2. List my players")
    print("  3. Edit starting 11")
    print(70 * "-")
    choice = input("  Enter number of menupoint: ")

    try:
        if choice == "back":
            print(fut_display.Bcolors.OKBLUE + "  Going back to FUT MENU" + fut_display.Bcolors.ENDC + '\n')
            fut_display.get_menu_choice()
        elif int(choice) == 1:
            list_owned_players('starting_11', True)
        elif int(choice) == 2:
            list_owned_players('owned_players', True)
        elif int(choice) == 3:
            edit_starting_eleven()
        else:
            print(fut_display.Bcolors.WARNING + "  No aspect found with number: " + choice + "!" + fut_display.Bcolors.ENDC)
            my_team()
    except ValueError:
        print(fut_display.Bcolors.WARNING + "  Aspect input must be a number! Given '" + choice + "' is wrong." + fut_display.Bcolors.ENDC)
        my_team()


def get_users_players_id(type_of_players):
    try:
        response = requests.get(fut_vars.users_URL, {'id': fut_login.user_id})
        user = response.json()
        if user:
            users_players = user[0][type_of_players]
            return users_players

    except requests.exceptions.Timeout as errt:
        print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
    except requests.exceptions.TooManyRedirects as errw:
        print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    except ValueError:
        print(fut_display.Bcolors.WARNING + "No JSON returned!" + fut_display.Bcolors.ENDC)

def list_owned_players(type_of_players, can_return):
    users_players = get_users_players_id(type_of_players)
    users_players_extended_list = []
    try:
        response = requests.get(fut_vars.players_URL, {'futbin_id': users_players})
        players = response.json()
        for i in range(len(players)):
            users_players_extended_list.append(players[i])

    except requests.exceptions.Timeout as errt:
        print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
    except requests.exceptions.TooManyRedirects as errw:
        print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    except ValueError:
        print(fut_display.Bcolors.WARNING + "No JSON returned!" + fut_display.Bcolors.ENDC)

    fut_display.show_players(users_players_extended_list)
    if can_return:
        my_team()

def edit_starting_eleven():
    print(fut_display.Bcolors.OKBLUE + "Your owned players" + fut_display.Bcolors.ENDC)
    list_owned_players('owned_players', False)
    print(fut_display.Bcolors.OKBLUE + "Your starting 11" + fut_display.Bcolors.ENDC)
    list_owned_players('starting_11', False)

    loop = True
    while loop:

        input_names = input("Enter the full name of players you want to change: ")
        players_to_sub = input_names.split(',')

        for i in range(len(players_to_sub)):
            players_to_sub[i] = players_to_sub[i].rstrip().lstrip()
            if players_to_sub[i] == "back":
                my_team()
        while "" in players_to_sub:
            players_to_sub.remove("")

        if len(players_to_sub) > 2 or len(players_to_sub) <= 1:
            print(fut_display.Bcolors.WARNING + "Changing requires 2 players separated with ','!" + fut_display.Bcolors.ENDC + '\n')
            edit_starting_eleven()

        try:
            response = requests.get(fut_vars.players_URL, {'player_extended_name': players_to_sub})
            players = response.json()
            players_futbin_id = []
            for i in range(len(players)):
                players_futbin_id.append(int(players[i]['futbin_id']))
            print(players_futbin_id)

            changing(players_futbin_id)

        except requests.exceptions.Timeout as errt:
            print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
        except requests.exceptions.TooManyRedirects as errw:
            print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except ValueError:
            print(fut_display.Bcolors.WARNING + "No JSON returned!" + fut_display.Bcolors.ENDC)

def changing(futbin_ids):
    owned = get_users_players_id('owned_players')
    starting = get_users_players_id('starting_11')

    found_counter = 0
    at_owned = {}
    for i in range(len(owned)):
        for j in range(len(futbin_ids)):
            if owned[i] == futbin_ids[j]:
                at_owned[i] = futbin_ids[j]
                found_counter = found_counter + 1

    at_starting = {}
    for i in range(len(starting)):
        for j in range(len(futbin_ids)):
            if starting[i] == futbin_ids[j]:
                at_starting[i] = futbin_ids[j]
                found_counter = found_counter + 1

    print(found_counter)
    if found_counter == 2:
        if len(at_starting) > len(at_owned):
            starting_ind = list(at_starting.keys())
            starting[int(starting_ind[0])] = at_starting[starting_ind[1]]
            starting[int(starting_ind[1])] = at_starting[starting_ind[0]]
            try:
                users_id_url = fut_vars.users_URL + '/' + str(fut_login.user_id)
                response = requests.post(users_id_url, {'starting_11': starting})

                if response.status_code == 404:
                    print(fut_display.Bcolors.WARNING + "URL not found!" + fut_display.Bcolors.ENDC)

            except requests.exceptions.Timeout as errt:
                print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
            except requests.exceptions.TooManyRedirects as errw:
                print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
        elif len(at_starting) < len(at_owned):
            owned_ind = list(at_owned.keys())
            owned[int(owned_ind[0])] = at_owned[owned_ind[1]]
            owned[int(owned_ind[1])] = at_owned[owned_ind[0]]
            try:
                users_id_url = fut_vars.users_URL + '/' + str(fut_login.user_id)
                response = requests.post(users_id_url, {'owned_players': owned})

                if response.status_code == 404:
                    print(fut_display.Bcolors.WARNING + "URL not found!" + fut_display.Bcolors.ENDC)

            except requests.exceptions.Timeout as errt:
                print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
            except requests.exceptions.TooManyRedirects as errw:
                print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
        else:
            owned_ind = list(at_owned.keys())
            starting_ind = list(at_starting.keys())
            owned[int(owned_ind[0])] = at_starting[starting_ind[0]]
            starting[int(starting_ind[0])] = at_owned[owned_ind[0]]
            try:
                users_id_url = fut_vars.users_URL + '/' + str(fut_login.user_id)
                print(users_id_url)
                response = requests.post(users_id_url, {'starting_11': starting})
                if response.status_code == 404:
                    print(fut_display.Bcolors.WARNING + "URL not found!" + fut_display.Bcolors.ENDC)
                    print(response.content)
                response = requests.post(users_id_url, {'owned_players': owned})
                if response.status_code == 404:
                    print(fut_display.Bcolors.WARNING + "URL not found!" + fut_display.Bcolors.ENDC)
                    print(response.content)

            except requests.exceptions.Timeout as errt:
                print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
            except requests.exceptions.TooManyRedirects as errw:
                print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
    else:
        print(fut_display.Bcolors.WARNING + "One of the names is misspelled!" + fut_display.Bcolors.ENDC)




# Nathan Aké, Allan Saint-Maximin
