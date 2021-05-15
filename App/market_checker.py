import request_try
import vars
from datetime import datetime
import display
import sell


def market_check():
    players_on_market = request_try.try_request_get(vars.market_URL, {'seller_id': vars.user_id})
    user = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})

    current_history = user[0]['history']
    if current_history:
        players_expired = []
        for item in players_on_market:
            expire_date = datetime.strptime(item['expire'], '%d/%m/%Y %H:%M:%S')
            if expire_date < datetime.now() and item['available'] == "True" and item['id'] in current_history:
                players_expired.append(item)

        if current_history:
            players_by_market_id = request_try.try_request_get(vars.market_URL, {'id': current_history})
            display.show_history(players_by_market_id)
            if players_expired:
                current_history = reserve_team_update(players_expired, current_history, user[0]['owned_players'], user[0]['starting_11'])
            history_patched = request_try.try_request_patch(vars.users_id_url, {'history': current_history})
            return True
    else:
        display.print_warning("You have no buy/sell history.")
        return False


def reserve_team_update(expired_players, history, user_owned_players_id, user_starting_11):
    user_owned_players = request_try.try_request_get(vars.players_URL, {'futbin_id': user_owned_players_id})
    user_starting_11_id = list(user_starting_11.values())
    user_starting_11 = request_try.try_request_get(vars.players_URL, {'futbin_id': user_starting_11_id})

    for player in expired_players:
        is_duplicate = False
        for owned_player in user_owned_players:
            if player['player_extended_name'] == owned_player['player_extended_name']:
                is_duplicate = True
                relisted = sell.relist(player)
                if relisted:
                    display.print_info_green("Player relisted on the market successfully!")
        for starting_player in user_starting_11:
            if player['player_extended_name'] == starting_player['player_extended_name']:
                is_duplicate = True
                relisted = sell.relist(player)
                if relisted:
                    display.print_info_green("Player relisted on the market successfully!")
        if not is_duplicate:
            user_owned_players_id.append(int(player['futbin_id']))
            if player['id'] in history:
                history.remove(player['id'])

    owned = user_owned_players_id
    request_try.try_request_patch(vars.users_id_url, {'owned_players': owned})
    return history
