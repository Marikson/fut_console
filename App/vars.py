
# start_server = ' json-server --watch multi_db.js --port 3000 '
players_URL = "http://localhost:3000/Players"
prices_URL = "http://localhost:3000/Prices"
users_URL = "http://localhost:3000/Users"
credentials_URL = 'http://localhost:3000/Credentials'
market_URL = 'http://localhost:3000/Market'
user_id = None
users_id_url = None
search_aspect = [{'player_name': "player name"},
                 {'quality': "quality"},
                 {'position': "position"},
                 {'nationality': "country"},
                 {'club': "club"},
                 {'revision': "rarity"},
                 {'league': "league"},
                 {'overall': "overall rating"}]
market_aspect = [{'player_name': "player name"},
                 {'quality': "quality"},
                 {'position': "position"},
                 {'nationality': "country"},
                 {'club': "club"},
                 {'revision': "rarity"},
                 {'league': "league"},
                 {'overall': "overall rating"},
                 {'min_price': "minimum price"},
                 {'max_price': "maximum price"}]


def set_user_vars(url, id):
    global user_id
    global users_id_url
    users_id_url = url
    user_id = id


"""
4418,      23859,       12676,
"""