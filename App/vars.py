
# start_server = ' json-server --watch multi_db.js --port 3000 '
players_URL = "http://localhost:3000/Players"
prices_URL = "http://localhost:3000/Prices"
users_URL = "http://localhost:3000/Users"
credentials_URL = 'http://localhost:3000/Credentials'
market_URL = 'http://localhost:3000/Market'
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
