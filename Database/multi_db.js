var Players  = require('./my_fut21_players.json');
var Prices = require('./my_fut21_prices.json');
var Credentials = require('./credentials.json');
var Users = require('./user_data.json');
var Market = require('./market.json');



module.exports  = () => ({
    FUT_21_Players: Players,
    FUT_21_Prices: Prices,
    Credentials: Credentials,
    Users: Users,
    Market: Market
  });