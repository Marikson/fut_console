import display
from datetime import datetime
import request_try
import vars


def get_coins():
    user = request_try.try_request_get(vars.users_URL, {"id": vars.user_id})
    return user[0]['coins']


def buy_player(params, min_price, max_price):
    market_players = request_try.try_request_get(vars.market_URL, params)
    selectable_market_ids = []
    if market_players:
        for item in list(market_players):
            expire_date = datetime.strptime(item['expire'], '%d/%m/%Y %H:%M:%S')
            if expire_date < datetime.now():
                market_players.remove(item)
            elif item['available'] == "False":
                market_players.remove(item)
            elif item['seller_id'] == vars.user_id:
                market_players.remove(item)
            elif min_price is not None:
                if item['price'] < int(min_price):
                    market_players.remove(item)
                else:
                    selectable_market_ids.append(item['id'])
            elif max_price is not None:
                if item['price'] > int(max_price):
                    market_players.remove(item)
                else:
                    selectable_market_ids.append(item['id'])
            else:
                selectable_market_ids.append(item['id'])
        if market_players:
            display.show_market_players(market_players)
            market_id = get_market_id(selectable_market_ids)
            if market_id in selectable_market_ids:
                double_check = buyable_check(market_id)
                if double_check:
                    user = request_try.try_request_get(vars.users_URL, {"id": vars.user_id})
                    history = user[0]['history']
                    history.append(market_id)
                    added_to_history = request_try.try_request_patch(vars.users_id_url, {'history': history})
                    print(display.Bcolors.OKGREEN + "      You bought the player!" + display.Bcolors.ENDC)
        else:
            print(display.Bcolors.OKCYAN + "      No matching player on the market with params above!" + display.Bcolors.ENDC + '\n')
            return
    else:
        print(display.Bcolors.OKCYAN + "      No matching player on the market with params above!" + display.Bcolors.ENDC + '\n')
        return


def get_market_id(selectable_market_ids):
    not_good = True
    while not_good:
        market_id_str = input("      Enter the the " + display.Bcolors.UNDERLINE + "Market ID" + display.Bcolors.ENDC + " of player you want to buy: ")
        if market_id_str == "back":
            print(display.Bcolors.OKBLUE + "      Going back to MARKET SEARCH" + display.Bcolors.ENDC + '\n')
            return False
        try:
            market_id = int(market_id_str)
            if market_id in selectable_market_ids:
                return market_id
            else:
                print(display.Bcolors.WARNING + "      The Market ID given is not valid!" + display.Bcolors.ENDC)
        except ValueError:
            print(display.Bcolors.WARNING + "      The Market ID given is not an integer!" + display.Bcolors.ENDC)


def buyable_check(market_id):
    player_to_buy = request_try.try_request_get(vars.market_URL, {'id': market_id})
    user = request_try.try_request_get(vars.users_URL, {"id": vars.user_id})
    buyable = False
    if player_to_buy[0]['available'] == "False":
        print(display.Bcolors.WARNING + "      The Market ID given is not valid!" + display.Bcolors.ENDC)
        return buyable
    if player_to_buy[0]['seller_id'] == vars.user_id:
        print(display.Bcolors.WARNING + "      The Market ID given is not valid!" + display.Bcolors.ENDC)
        return buyable
    expire_date = datetime.strptime(player_to_buy[0]['expire'], '%d/%m/%Y %H:%M:%S')
    if expire_date < datetime.now():
        print(display.Bcolors.WARNING + "      There is no player on the market with Market ID: " + str(market_id) + display.Bcolors.ENDC)
        return buyable
    user_owned_players_id = user[0]['owned_players']
    if user_owned_players_id:
        user_owned_players = request_try.try_request_get(vars.players_URL, {'futbin_id': user_owned_players_id})
        for i in range(len(user_owned_players)):
            if player_to_buy[0]['player_extended_name'] == user_owned_players[i]['player_extended_name']:
                print(display.Bcolors.WARNING + "      You already own " + player_to_buy[0]['player_extended_name'] + "!" + display.Bcolors.ENDC)
                return buyable
    user_starting_11_id = user[0]['starting_11']
    if user_starting_11_id:
        user_starting_players = request_try.try_request_get(vars.players_URL, {'futbin_id': user_starting_11_id})
        for i in range(len(user_starting_players)):
            if player_to_buy[0]['player_extended_name'] == user_starting_players[i]['player_extended_name']:
                print(display.Bcolors.WARNING + "      You already own " + player_to_buy[0]['player_extended_name'] + "!" + display.Bcolors.ENDC)
                return buyable
    if int(player_to_buy[0]['price']) > int(user[0]['coins']):
        print(display.Bcolors.WARNING + "      You do not have enough coins!" + display.Bcolors.ENDC)
        print(display.Bcolors.OKCYAN + "      Your coins: " + str(user[0]['coins']) + ", players price: " + str(player_to_buy[0]['price']) + display.Bcolors.ENDC + '\n')
        return buyable
    else:
        buyable = True
    buyed = False
    if buyable:
        user_owned_players_id.append(int(player_to_buy[0]['futbin_id']))
        owned = user_owned_players_id
        added_to_owned = request_try.try_request_patch(vars.users_id_url, {'owned_players': owned})

        coin_remained = int(user[0]['coins']) - int(player_to_buy[0]['price'])
        coin_minus = request_try.try_request_patch(vars.users_id_url, {'coins': coin_remained})

        seller_user = request_try.try_request_get(vars.users_URL, {"id": player_to_buy[0]['seller_id']})
        seller_user_url = vars.users_URL + '/' + str(player_to_buy[0]['seller_id'])
        seller_coin = int(seller_user[0]['coins']) + int(player_to_buy[0]['price'])
        coin_plus = request_try.try_request_patch(seller_user_url, {'coins': seller_coin})

        market_id_url = vars.market_URL + '/' + str(market_id)
        set_unavailable = request_try.try_request_patch(market_id_url, {'available': "False"})

        if added_to_owned + coin_minus + set_unavailable + coin_plus:
            buyed = True
    return buyable + buyed

