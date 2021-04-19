import request_try
import vars
import login
from datetime import datetime
import display
import sell

def market_check():
    players_on_market = request_try.try_request_get(vars.market_URL, {'seller_id': login.user_id})
    user = request_try.try_request_get(vars.users_URL, {'id': login.user_id})
    current_history = user[0]['history']
    players_to_history = []
    players_expired = []
    for item in players_on_market:
        current_history.append(item['id'])
        expire_date = datetime.strptime(item['expire'], '%d/%m/%Y %H:%M:%S')
        if expire_date < datetime.now():
            players_expired.append(item)

    if players_expired:
        reserve_team_update(players_expired)

    added_to_history = request_try.try_request_patch(login.users_id_url, {'history': current_history})
    if current_history:
        players_by_market_id = request_try.try_request_get(vars.market_URL, {'id': current_history})
        display.show_history(players_by_market_id)
    else:
        print(display.Bcolors.WARNING + "You have no buy/sell history." + display.Bcolors.ENDC)


def reserve_team_update(expired_players):
    user = request_try.try_request_get(vars.users_URL, {"id": login.user_id})
    user_owned_players_id = user[0]['owned_players']
    for player in expired_players:
        if int(player['futbin_id']) in user_owned_players_id:
            sell.relist(player)
        else:
            user_owned_players_id.append(int(player['futbin_id']))
    owned = user_owned_players_id
    request_try.try_request_patch(login.users_id_url, {'owned_players': owned})




#user2 owned [8388, 25655, 20688, 23300, 20593, 4410],