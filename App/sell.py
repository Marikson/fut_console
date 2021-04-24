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
            if name_to_sell == "back":
                display.print_info("Going back to FUT MENU")
                return False
            name_to_sell = name_to_sell.rstrip().lstrip()
            players_with_name_to_sell = request_try.try_request_get(vars.players_URL, {'player_extended_name': name_to_sell})

            fbid_with_rsid = {}
            for i in range(len(players_with_name_to_sell)):
                fbid_with_rsid[int(players_with_name_to_sell[i]['futbin_id'])] = int(players_with_name_to_sell[i]['resource_id'])

            futbin_ids = list(fbid_with_rsid.keys())
            matched = list_players.select_matching(futbin_ids, "owned_players")
            if matched.found_counter == 1:
                owned_player_ids = matched.ids
                index_id_pair = matched.at_ind
                index_to_remove = list(index_id_pair.keys())
                player_to_sell_id = list(index_id_pair.values())
                del owned_player_ids[index_to_remove[0]]
                get_price_advice(fbid_with_rsid[player_to_sell_id[0]])
                price = set_price()
                if price:
                    full_player_to_sell = request_try.try_request_get(vars.players_URL, {'futbin_id': player_to_sell_id[0]})
                    player_to_market = add_market_data(full_player_to_sell[0], price)
                    advertised = request_try.try_request_post(vars.market_URL, player_to_market)
                    removed = request_try.try_request_patch(vars.users_id_url, {'owned_players': owned_player_ids})
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


def set_price():
    price_not_good = True
    while price_not_good:
        str_price = input("Enter the price you want to sell your player for: ")
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
        full_player_to_sell = player
        get_price_advice(player['resource_id'])
        price = set_price()
        if price:
            full_player_to_sell['price'] = price
            full_player_to_sell['seller_id'] = vars.user_id
            expire_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            str_expire_time = str(expire_time.strftime("%d/%m/%Y %H:%M:%S"))
            full_player_to_sell['expire'] = str_expire_time
            full_player_to_sell['available'] = "True"
            listed_player_url = vars.market_URL + '/' + str(full_player_to_sell['id'])
            advertised = request_try.try_request_patch(listed_player_url, {'price': price, 'expire': str_expire_time, 'available': "True"})
            if advertised:
                display.print_info_green("Player relisted on the market successfully!")
                return
            else:
                display.print_warning("Listing on the market failed!")
        else:
            return
