import display
import vars
import request_try
import list_players
import datetime


def sell_player():
    stay = True
    while stay:
        if list_players.list_owned_players():
            name_to_sell = input("Enter the " + display.Bcolors.UNDERLINE + "full name" + display.Bcolors.ENDC + " of player you want to sell: ")
            name_to_sell = name_to_sell.rstrip().lstrip()
            if name_to_sell == "back":
                display.print_info("Going back to FUT MENU")
                return False
            players_with_name_to_sell = request_try.try_request_get(vars.players_URL, {'player_extended_name': name_to_sell})
            fbid_with_rsid = futbin_ids_with_resource_ids(players_with_name_to_sell)
            futbin_ids = list(fbid_with_rsid.keys())
            found_at_owned = list_players.select_matching(futbin_ids, "owned_players")
            if found_at_owned.found_counter == 1:
                player_to_sell_id = get_player_to_sell_id(found_at_owned)
                owned_without_player_to_sell = remove_from_owned(found_at_owned)
                get_price_advice(fbid_with_rsid[player_to_sell_id])
                price = set_price()
                if price:
                    removed = patch_owned(owned_without_player_to_sell)
                    advertised = put_player_to_market(player_to_sell_id, price)
                    if advertised and removed:
                        display.print_info_green("Player listed on the market successfully!")
                        return True
                    else:
                        display.print_warning("Listing on the market failed!")
            else:
                display.print_warning("The name given is probably misspelled!")
        else:
            display.print_warning("  Selling only possible from Reserve Team.")
            return False


def get_player_to_sell_id(found_at_owned):
    player_to_sell_id = list(found_at_owned.at_ind.values())
    return player_to_sell_id[0]


def remove_from_owned(found_at_owned):
    index_to_remove = list(found_at_owned.at_ind.keys())
    del found_at_owned.ids[index_to_remove[0]]
    return found_at_owned.ids


def futbin_ids_with_resource_ids(players_with_name_to_sell):
    fbid_with_rsid = {}
    for i in range(len(players_with_name_to_sell)):
        fbid_with_rsid[int(players_with_name_to_sell[i]['futbin_id'])] = int(players_with_name_to_sell[i]['resource_id'])
    return fbid_with_rsid


def put_player_to_market(id, price):
    full_player_to_sell = request_try.try_request_get(vars.players_URL, {'futbin_id': id})
    player_to_market = add_market_data(full_player_to_sell[0], price)
    advertised = request_try.try_request_post(vars.market_URL, player_to_market)
    added_to_history = add_to_history()
    return advertised and added_to_history


def add_to_history():
    users_players_on_market = request_try.try_request_get(vars.market_URL, {'seller_id': vars.user_id})
    users_last_player_on_market = users_players_on_market[-1]
    user = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
    current_history = user[0]['history']
    current_history.append(users_last_player_on_market['id'])
    added_to_history = request_try.try_request_patch(vars.users_id_url, {'history': current_history})
    return added_to_history


def patch_owned(owned):
    removed = request_try.try_request_patch(vars.users_id_url, {'owned_players': owned})
    return removed


def set_price():
    price_not_good = True
    while price_not_good:
        str_price = input("Enter the price you want to sell your player for: ")
        str_price = str_price.rstrip().lstrip()
        if str_price == "back":
            display.print_info("Going back to SELLING PLAYER")
            return False
        try:
            price = int(str_price)
            if price > 0:
                return price
            else:
                display.print_warning("Price needs to be positive!")
        except ValueError:
            display.print_warning("The price given is not an integer!")


def get_price_advice(resource_id):
    prices = request_try.try_request_get(vars.prices_URL, {'resource_id': resource_id})
    sum_price = 0
    all_prices = []
    if prices:
        for date in prices[0]['dates']:
            sum_price = sum_price + int(prices[0]['dates'][date]['ps4'])
            all_prices.append(int(prices[0]['dates'][date]['ps4']))

        all_dates = list(prices[0]['dates'].keys())
        avg_price = int(sum_price / len(prices[0]['dates']))

        min_data = {'date': "-",
                    'price': None}
        for date in prices[0]['dates']:
            if not min_data['price']:
                min_data['price'] = int(prices[0]['dates'][date]['ps4'])
                min_data['date'] = date
            elif min_data['price'] >= int(prices[0]['dates'][date]['ps4']):
                min_data['price'] = int(prices[0]['dates'][date]['ps4'])
                min_data['date'] = date

        max_data = {'date': "-",
                    'price': None}
        for date in prices[0]['dates']:
            if not max_data['price']:
                max_data['price'] = int(prices[0]['dates'][date]['ps4'])
                max_data['date'] = date
            elif max_data['price'] <= int(prices[0]['dates'][date]['ps4']):
                max_data['price'] = int(prices[0]['dates'][date]['ps4'])
                max_data['date'] = date
        display.show_price_advice(avg_price, min_data, max_data, all_prices, all_dates)
    else:
        display.print_info("There is no market data for this player.")


def add_market_data(player, price):
    player['price'] = price
    player['seller_id'] = vars.user_id
    expire_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    str_expire_time = str(expire_time.strftime("%d/%m/%Y %H:%M:%S"))
    player['expire'] = str_expire_time
    player['available'] = "True"
    return player


def relist(player):
    not_relisted = True
    while not_relisted:
        warning_string = "Nobody bought your player, and you can not have a duplicate of " + player['player_extended_name']
        display.print_warning(warning_string)
        get_price_advice(player['resource_id'])
        price = set_price()
        if price:
            expire_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            str_expire_time = str(expire_time.strftime("%d/%m/%Y %H:%M:%S"))
            listed_player_url = vars.market_URL + '/' + str(player['id'])
            advertised = request_try.try_request_patch(listed_player_url, {'price': price, 'expire': str_expire_time, 'available': "True"})
            if advertised:
                return True
            else:
                display.print_warning("Listing on the market failed!")
        else:
            return False
