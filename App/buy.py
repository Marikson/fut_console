import display
from datetime import datetime
import request_try
import vars


def get_coins():
    user = request_try.try_request_get(vars.users_URL, {"id": vars.user_id})
    return user[0]['coins']


def buy_player(params, min_price, max_price):
    market_players = request_try.try_request_get(vars.market_URL, params)
    if market_players:
        filtered_market_players = filter_market_players(market_players, min_price, max_price)
        if filtered_market_players:
            display.show_market_players(filtered_market_players)
            selectable_market_ids = create_selectable_market_ids(filtered_market_players)
            market_id = get_market_id(selectable_market_ids)
            if market_id in selectable_market_ids:
                double_check = buyable_check(market_id)
                if double_check:
                    display.print_info_green("      You bought the player!")
        else:
            display.print_info_cyan("      No matching player on the market with params above!")
            return False
    else:
        display.print_info_cyan("      No matching player on the market with params above!")
        return False


def create_selectable_market_ids(filtered_market_players):
    selectable_market_ids = []
    for item in filtered_market_players:
        selectable_market_ids.append(item['id'])
    return selectable_market_ids


def filter_market_players(market_players, min_price, max_price):
    for item in list(market_players):
        expire_date = datetime.strptime(item['expire'], '%d/%m/%Y %H:%M:%S')
        if expire_date < datetime.now():
            market_players.remove(item)
        elif item['available'] == "False":
            market_players.remove(item)
        elif item['seller_id'] == vars.user_id:
            market_players.remove(item)
        elif min_price is not None or max_price is not None:
            if min_price is not None:
                if item['price'] < int(min_price):
                    market_players.remove(item)
            if max_price is not None:
                if item['price'] > int(max_price):
                    market_players.remove(item)
    return market_players

def get_market_id(selectable_market_ids):
    not_good = True
    while not_good:
        market_id_str = input("      Enter the the " + display.Bcolors.UNDERLINE + "Market ID" + display.Bcolors.ENDC + " of player you want to buy: ")
        if market_id_str == "back":
            display.print_info("      Going back to MARKET SEARCH")
            return False
        try:
            market_id = int(market_id_str)
            if market_id in selectable_market_ids:
                return market_id
            else:
                display.print_warning("      The Market ID given is not valid!")
        except ValueError:
            display.print_warning("      The Market ID given is not an integer!")


def buyable_check(market_id):
    player_to_buy = request_try.try_request_get(vars.market_URL, {'id': market_id})
    user = request_try.try_request_get(vars.users_URL, {"id": vars.user_id})
    buyable = False
    if player_to_buy[0]['available'] == "False":
        display.print_warning("      The Market ID given is not valid!")
        return buyable
    if player_to_buy[0]['seller_id'] == vars.user_id:
        display.print_warning("      The Market ID given is not valid!")
        return buyable
    expire_date = datetime.strptime(player_to_buy[0]['expire'], '%d/%m/%Y %H:%M:%S')
    if expire_date < datetime.now():
        warning_string = "      There is no player on the market with Market ID: " + str(market_id)
        display.print_warning(warning_string)
        return buyable
    user_owned_players_id = user[0]['owned_players']
    if user_owned_players_id:
        user_owned_players = request_try.try_request_get(vars.players_URL, {'futbin_id': user_owned_players_id})
        for i in range(len(user_owned_players)):
            if player_to_buy[0]['player_extended_name'] == user_owned_players[i]['player_extended_name']:
                warning_string = "      You already own " + player_to_buy[0]['player_extended_name'] + "!"
                display.print_warning(warning_string)
                return buyable
    user_starting_11_id = user[0]['starting_11']
    if user_starting_11_id:
        user_starting_players = request_try.try_request_get(vars.players_URL, {'futbin_id': user_starting_11_id})
        for i in range(len(user_starting_players)):
            if player_to_buy[0]['player_extended_name'] == user_starting_players[i]['player_extended_name']:
                warning_string = "      You already own " + player_to_buy[0]['player_extended_name'] + "!"
                display.print_warning(warning_string)
                return buyable
    if int(player_to_buy[0]['price']) > int(user[0]['coins']):
        display.print_warning("      You do not have enough coins!")
        info_string = "      Your coins: " + str(user[0]['coins']) + ", players price: " + str(player_to_buy[0]['price'])
        display.print_info_cyan(info_string)
        return buyable
    else:
        buyable = True
    bought = False
    if buyable:
        transaction_succeded = transaction(user_owned_players_id, user[0], player_to_buy[0], market_id)
        if transaction_succeded:
            bought = True
    return buyable and bought


def transaction(user_owned_players_id, user, player_to_buy, market_id):
    user_owned_players_id.append(int(player_to_buy['futbin_id']))
    owned = user_owned_players_id
    added_to_owned = request_try.try_request_patch(vars.users_id_url, {'owned_players': owned})

    coin_remained = int(user['coins']) - int(player_to_buy['price'])
    coin_minus = request_try.try_request_patch(vars.users_id_url, {'coins': coin_remained})

    seller_user = request_try.try_request_get(vars.users_URL, {"id": player_to_buy['seller_id']})
    seller_user_url = vars.users_URL + '/' + str(player_to_buy['seller_id'])
    seller_coin = int(seller_user[0]['coins']) + int(player_to_buy['price'])
    coin_plus = request_try.try_request_patch(seller_user_url, {'coins': seller_coin})

    market_id_url = vars.market_URL + '/' + str(market_id)
    set_unavailable = request_try.try_request_patch(market_id_url, {'available': "False"})

    added_to_history = add_to_history(user, market_id)
    if added_to_owned and coin_minus and coin_plus and set_unavailable and added_to_history:
        return True
    else:
        return False


def add_to_history(user, market_id):
    history = user['history']
    int_market_id = int(market_id)
    history.append(int_market_id)
    added_to_history = request_try.try_request_patch(vars.users_id_url, {'history': history})
    return added_to_history
