import display
import login
import vars
import request_try
import list_players
import datetime


def sell_player():
    stay = True
    while stay:
        list_players.list_owned_players()
        name_to_sell = input("Enter the full name of player you want to sell: ")
        if name_to_sell == "back":
            print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
            return
        name_to_sell = name_to_sell.rstrip().lstrip()
        players_with_name_to_sell = request_try.try_request_get(vars.players_URL, {'player_extended_name': name_to_sell})

        fbid_with_rsid = {}
        for i in range(len(players_with_name_to_sell)):
            fbid_with_rsid[int(players_with_name_to_sell[i]['futbin_id'])] = int(players_with_name_to_sell[i]['resource_id'])

        futbin_ids = list(fbid_with_rsid.keys())
        matched = list_players.select_matching(futbin_ids, "owned_players")
        if matched.found_counter == 1:
            owned = matched.ids
            at_ind = matched.at_ind
            ind = list(at_ind.keys())
            val = list(at_ind.values())
            del owned[ind[0]]
            get_price_advice(fbid_with_rsid[val[0]])
            price = set_price()
            if price:
                full_player_to_sell = request_try.try_request_get(vars.players_URL, {'futbin_id': futbin_ids[0]})
                full_player_to_sell[0]['price'] = price
                full_player_to_sell[0]['seller'] = login.user_id
                full_player_to_sell[0]['available'] = str((datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat())

                advertised = request_try.try_request_post(vars.market_URL, full_player_to_sell[0])
                removed = request_try.try_request_patch(login.users_id_url, {'owned_players': owned})
                if advertised and removed:
                    print(display.Bcolors.OKGREEN + "Player listed on the market successfully!" + display.Bcolors.ENDC)
                else:
                    print(display.Bcolors.WARNING + "Listing on the market failed!" + display.Bcolors.ENDC)
            else:
                return
        else:
            print(display.Bcolors.WARNING + "The name given is probably misspelled!" + display.Bcolors.ENDC)


def set_price():
    price_not_good = True
    while price_not_good:
        str_price = input("Enter the price you want to sell your player for: ")
        if str_price == "back":
            print(display.Bcolors.OKBLUE + "  Going back to FUT MENU" + display.Bcolors.ENDC + '\n')
            return False
        try:
            price = int(str_price)
            if price:
                return price
        except ValueError:
            print(display.Bcolors.WARNING + "The price given is not an integer!" + display.Bcolors.ENDC)



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