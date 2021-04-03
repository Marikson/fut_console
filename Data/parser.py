import csv
import random
from csv import reader
import json
import collections


# Gettiing players
playerStats = []
playersFile = 'fut_bin21_players.csv'
with open(playersFile, newline='', encoding='utf-8') as f:
  playerReader = csv.reader(f)
  ColumnsArray = next(playerReader)
  ColumnsString = ''.join(ColumnsArray)
  playerColumns = ColumnsString.split(';')
  StatsArray = list(playerReader)
  for i in range(len(StatsArray)):
    StatsString = ''.join(StatsArray[i])
    playerStats.append(StatsString.split(';'))


# player_dict = collections.defaultdict(dict)
player_dict = [dict() for x in range(len(playerStats))]
for i in range(len(playerStats)):
    for j in range(len(playerColumns)):
        player_dict[i][playerColumns[j]] = playerStats[i][j]

print(player_dict[5])
print(playerStats[5])
print(playerStats[5][0])

dict_players = {
    'Players': player_dict
}

members = random.randint(80,300)
just_player_ids = []
for i in range(len(playerStats)):
    just_player_ids.append(int(playerStats[i][0]))

print(len(just_player_ids))

team = random.sample(just_player_ids, members)
print(team)
print(len(team))

"""
# Gettign prices
prices = [] 
pricesFile = 'fut_bin21_prices.csv'
with open(pricesFile, newline='', encoding='utf-8') as f:
  priceReader = csv.reader(f)
  ColumnsArray = next(priceReader)
  ColumnsString = ''.join(ColumnsArray)
  pricesColumns = ColumnsString.split(';')
  PricesArray = list(priceReader)
  for i in range(len(PricesArray)):
    PricesString = ''.join(PricesArray[i])
    prices.append(PricesString.split(';'))

print(pricesColumns)
print(prices[0])

prices_dict = [dict() for x in range(len(prices))]
for i in range(len(prices)):
    for j in range(len(pricesColumns)):
        prices_dict[i][pricesColumns[j]] = prices[i][j]

print(prices_dict[0])
print(prices_dict[1])
print(prices_dict[2])
print(prices_dict[3])
print(len(prices_dict))

only_prices = [dict() for x in range(len(prices))]
for i in range(len(prices)):
    for j in range(2,len(pricesColumns)):
        only_prices[i][pricesColumns[j]] = prices[i][j]

dict_prices = []
resId = -1
temp_dict = dict()
# print(temp_dict)
for i in range(len(prices_dict)): 
    if (prices_dict[i]['resource_id'] != resId):
        if (temp_dict):
            # print(temp_dict)
            dict_prices.append(temp_dict)
        temp_dict = {}
        resId = prices_dict[i]['resource_id']
        temp_dict['resource_id'] = resId
        temp_dict['dates'] = dict()
    temp_dict['dates'][ prices_dict[i]['date'] ] = only_prices[i]


print(len(dict_prices))
print(dict_prices[0])
print(dict_prices[1])
print(dict_prices[2])
print(dict_prices[3])


final_prices_dict = {
    "Prices": dict_prices
}



with open("my_fut21_prices.json", "w") as outfile:
    json.dump(dict_prices, outfile)
"""