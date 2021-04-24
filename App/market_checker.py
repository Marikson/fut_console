import request_try
import vars
from datetime import datetime
import display
import sell


def market_check():
    players_on_market = request_try.try_request_get(vars.market_URL, {'seller_id': vars.user_id})
    user = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})

    current_history = user[0]['history']
    if players_on_market or current_history:
        players_expired = []
        for item in players_on_market:
            expire_date = datetime.strptime(item['expire'], '%d/%m/%Y %H:%M:%S')
            if item['id'] in current_history:
                if expire_date < datetime.now() and item['available'] == "True":
                    players_expired.append(item)
            elif expire_date < datetime.now() and item['available'] == "True":
                pass
            else:
                current_history.append(item['id'])

        if current_history:
            players_by_market_id = request_try.try_request_get(vars.market_URL, {'id': current_history})
            display.show_history(players_by_market_id)
            if players_expired:
                current_history = reserve_team_update(players_expired, current_history, user[0]['owned_players'])
            history_patched = request_try.try_request_patch(vars.users_id_url, {'history': current_history})
    else:
        display.print_warning("You have no buy/sell history.")


def reserve_team_update(expired_players, history, user_owned_players_id):
    for player in expired_players:
        if int(player['futbin_id']) in user_owned_players_id:
            sell.relist(player)
        else:
            user_owned_players_id.append(int(player['futbin_id']))
            history.remove(player['id'])
    owned = user_owned_players_id
    request_try.try_request_patch(vars.users_id_url, {'owned_players': owned})
    return history
