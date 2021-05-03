import display
import vars
import request_try
import collections


def get_users_players_id(type_of_players):
    user = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
    if user:
        users_players = user[0][type_of_players]
        return users_players


def list_owned_players():
    users_players = get_users_players_id('owned_players')
    users_players_extended_list = []
    players = request_try.try_request_get(vars.players_URL, {'futbin_id': users_players})

    for i in range(len(players)):
        users_players_extended_list.append(players[i])

    if users_players:
        display.print_info("Your Reserve Team")
        display.show_players(users_players_extended_list)
        return True
    else:
        display.print_warning("  You have no players in your Reserve Team.")
        return False


def list_starting_11():
    users_players = get_users_players_id('starting_11')
    users_players_extended_list = []
    positions = list(users_players.keys())
    users_players_id = list(users_players.values())

    players = request_try.try_request_get(vars.players_URL, {'futbin_id': users_players_id})
    for j in positions:
        for i in range(len(players)):
            if int(players[i]['futbin_id']) == users_players[j]:
                players[i]['POS'] = j
                users_players_extended_list.append(players[i])

    display.print_info("Your Starting 11")
    display.show_starting_11(users_players_extended_list, positions)


def select_matching(searched_futbin_ids, type_of_players):
    ids = get_users_players_id(type_of_players)
    if type(ids) is dict:
        sequence = list(ids.keys())
    else:
        sequence = range(len(ids))

    found_counter = 0
    at_ind = {}
    for i in sequence:
        for j in range(len(searched_futbin_ids)):
            if ids[i] == searched_futbin_ids[j]:
                at_ind[i] = searched_futbin_ids[j]
                found_counter = found_counter + 1

    Matched = collections.namedtuple('Matched', ['at_ind', 'found_counter', 'ids'])
    matched = Matched(at_ind, found_counter, ids)
    return matched

