from prettytable import PrettyTable
import termplotlib
import vars
from datetime import datetime

class Bcolors:
    HEADER = '\033[95m'
    MAGENTA = '\033[35m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WWHITE = '\033[97m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    LIGHTRED = '\033[91m'
    UNDERLINE = '\033[4m'


def show_starting_11(players_list, positions):
    player_rows = ["POS", "Name", "Overall rating", "Preferred Position", "Nationality", "Club", "Rarity", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"]
    spreadsheet = PrettyTable(player_rows)
    for j in range(len(positions)):
        for i in range(len(players_list)):
            if players_list[i]['POS'] == positions[j]:
                color = Bcolors.ENDC
                if players_list[i]['quality'] == "Gold - Rare" or players_list[i]['quality'] == "Gold - Non-Rare":
                    color = Bcolors.WARNING
                elif players_list[i]['quality'] == "Silver - Rare" or players_list[i]['quality'] == "Silver - Non-Rare":
                    color = Bcolors.WWHITE
                elif players_list[i]['quality'] == "Bronze - Rare" or players_list[i]['quality'] == "Bronze - Non-Rare":
                    color = Bcolors.ENDC
                if players_list[i]['revision'] == "CL":
                    color = Bcolors.OKBLUE
                if players_list[i]['revision'] == "OTW":
                    color = Bcolors.OKGREEN
                if players_list[i]['revision'] == 'IF':
                    color = Bcolors.OKCYAN
                if players_list[i]['revision'] == 'Icon':
                    color = Bcolors.MAGENTA
                if players_list[i]['position'] == "GK":
                    attributes = [positions[j],
                                  color + players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['revision'],
                                  players_list[i]['gk_diving'],
                                  players_list[i]['gk_handling'],
                                  players_list[i]['gk_kicking'],
                                  players_list[i]['gk_reflexes'],
                                  players_list[i]['gk_speed'],
                                  players_list[i]['gk_positoning'] + Bcolors.ENDC]
                else:
                    attributes = [positions[j],
                                  color + players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['revision'],
                                  players_list[i]['pace'],
                                  players_list[i]['shooting'],
                                  players_list[i]['passing'],
                                  players_list[i]['dribbling'],
                                  players_list[i]['defending'],
                                  players_list[i]['physicality'] + Bcolors.ENDC]
                spreadsheet.add_row(attributes)

    print(spreadsheet)


def show_players(players_list):
    player_rows = ["Name", "Overall rating", "Position", "Nationality", "Club", "Rarity", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"]
    spreadsheet = PrettyTable(player_rows)
    for i in range(len(players_list)):
        color = Bcolors.ENDC
        if players_list[i]['quality'] == "Gold - Rare" or players_list[i]['quality'] == "Gold - Non-Rare":
            color = Bcolors.WARNING
        elif players_list[i]['quality'] == "Silver - Rare" or players_list[i]['quality'] == "Silver - Non-Rare":
            color = Bcolors.WWHITE
        elif players_list[i]['quality'] == "Bronze - Rare" or players_list[i]['quality'] == "Bronze - Non-Rare":
            color = Bcolors.ENDC
        if players_list[i]['revision'] == "CL":
            color = Bcolors.OKBLUE
        if players_list[i]['revision'] == "OTW":
            color = Bcolors.OKGREEN
        if players_list[i]['revision'] == 'IF':
            color = Bcolors.OKCYAN
        if players_list[i]['revision'] == 'Icon':
            color = Bcolors.MAGENTA

        if players_list[i]['position'] == "GK":
            attributes = [color + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['revision'],
                          players_list[i]['gk_diving'],
                          players_list[i]['gk_handling'],
                          players_list[i]['gk_kicking'],
                          players_list[i]['gk_reflexes'],
                          players_list[i]['gk_speed'],
                          players_list[i]['gk_positoning'] + Bcolors.ENDC]
        else:
            attributes = [color + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['revision'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'] + Bcolors.ENDC]

        spreadsheet.add_row(attributes)

    print(spreadsheet)


def show_market_players(players_list):
    player_rows = ["Market ID", "Name", "Overall rating", "Position", "Nationality", "Club", "Rarity", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality", "Price", "Expire"]
    spreadsheet = PrettyTable(player_rows)
    for i in range(len(players_list)):
        color = Bcolors.ENDC
        if players_list[i]['quality'] == "Gold - Rare" or players_list[i]['quality'] == "Gold - Non-Rare":
            color = Bcolors.WARNING
        elif players_list[i]['quality'] == "Silver - Rare" or players_list[i]['quality'] == "Silver - Non-Rare":
            color = Bcolors.WWHITE
        elif players_list[i]['quality'] == "Bronze - Rare" or players_list[i]['quality'] == "Bronze - Non-Rare":
            color = Bcolors.ENDC
        if players_list[i]['revision'] == "CL":
            color = Bcolors.OKBLUE
        if players_list[i]['revision'] == "OTW":
            color = Bcolors.OKGREEN
        if players_list[i]['revision'] == 'IF':
            color = Bcolors.OKCYAN
        if players_list[i]['revision'] == 'Icon':
            color = Bcolors.MAGENTA

        if players_list[i]['position'] == "GK":
            attributes = [str(players_list[i]['id']),
                          color + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['revision'],
                          players_list[i]['gk_diving'],
                          players_list[i]['gk_handling'],
                          players_list[i]['gk_kicking'],
                          players_list[i]['gk_reflexes'],
                          players_list[i]['gk_speed'],
                          players_list[i]['gk_positoning'],
                          players_list[i]['price'],
                          players_list[i]['expire'] + Bcolors.ENDC]
        else:
            attributes = [str(players_list[i]['id']),
                          color + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['revision'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'],
                          players_list[i]['price'],
                          players_list[i]['expire'] + Bcolors.ENDC]

        spreadsheet.add_row(attributes)

    print(spreadsheet)


def show_extended_players(players_list):
    main_rows = ["Name", "Overall", "Acceleration", "Sprint speed", "Positioning", "Finishing", "Shot power", "Penalties", "Free kick", "Crossing", "Long pass", "Short passs", "Ball controll", "Reactions", "Interceptions", "Marking", "Strength", "Stamina"]
    spreadsheet = PrettyTable(main_rows)
    for i in range(len(players_list)):
        color = Bcolors.ENDC
        if players_list[i]['quality'] == "Gold - Rare" or players_list[i]['quality'] == "Gold - Non-Rare":
            color = Bcolors.WARNING
        elif players_list[i]['quality'] == "Silver - Rare" or players_list[i]['quality'] == "Silver - Non-Rare":
            color = Bcolors.WWHITE
        elif players_list[i]['quality'] == "Bronze - Rare" or players_list[i]['quality'] == "Bronze - Non-Rare":
            color = Bcolors.ENDC
        if players_list[i]['revision'] == "CL":
            color = Bcolors.OKBLUE
        if players_list[i]['revision'] == "OTW":
            color = Bcolors.OKGREEN
        if players_list[i]['revision'] == 'IF':
            color = Bcolors.OKCYAN
        if players_list[i]['revision'] == 'Icon':
            color = Bcolors.MAGENTA
        attributes = [color + players_list[i]['player_extended_name'],
                      players_list[i]['overall'],
                      players_list[i]['pace_acceleration'],
                      players_list[i]['pace_sprint_speed'],
                      players_list[i]['shoot_positioning'],
                      players_list[i]['shoot_finishing'],
                      players_list[i]['shoot_shot_power'],
                      players_list[i]['shoot_penalties'],
                      players_list[i]['pass_free_kick'],
                      players_list[i]['pass_crossing'],
                      players_list[i]['pass_long'],
                      players_list[i]['pass_short'],
                      players_list[i]['drib_ball_control'],
                      players_list[i]['drib_reactions'],
                      players_list[i]['def_interceptions'],
                      players_list[i]['def_marking'],
                      players_list[i]['phys_strength'],
                      players_list[i]['phys_stamina'] + Bcolors.ENDC]

        spreadsheet.add_row(attributes)

    print(spreadsheet)


def show_price_advice(avgp, minp, maxp, prices, dates):
    fig = termplotlib.figure()
    fig.barh(prices, dates, force_ascii=True)
    fig.show()

    main_rows = ["Average price", "Lowest price", "Lowest price date", "Highest price", "Highest price date"]
    spreadsheet = PrettyTable(main_rows)
    data = [avgp,
            minp['price'],
            minp['date'],
            maxp['price'],
            maxp['date']]
    spreadsheet.add_row(data)
    print(spreadsheet)


def show_history(players_list):
    player_rows = ["Status", "Price", "Name", "Overall rating", "Position", "Nationality", "Club", "Rarity", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"]
    spreadsheet = PrettyTable(player_rows)
    for i in range(len(players_list)):
        color = Bcolors.ENDC
        if players_list[i]['quality'] == "Gold - Rare" or players_list[i]['quality'] == "Gold - Non-Rare":
            color = Bcolors.WARNING
        elif players_list[i]['quality'] == "Silver - Rare" or players_list[i]['quality'] == "Silver - Non-Rare":
            color = Bcolors.WWHITE
        elif players_list[i]['quality'] == "Bronze - Rare" or players_list[i]['quality'] == "Bronze - Non-Rare":
            color = Bcolors.ENDC
        if players_list[i]['revision'] == "CL":
            color = Bcolors.OKBLUE
        if players_list[i]['revision'] == "OTW":
            color = Bcolors.OKGREEN
        if players_list[i]['revision'] == 'IF':
            color = Bcolors.OKCYAN
        if players_list[i]['revision'] == 'Icon':
            color = Bcolors.MAGENTA

        expire_date = datetime.strptime(players_list[i]['expire'], '%d/%m/%Y %H:%M:%S')
        if players_list[i]['seller_id'] == vars.user_id and players_list[i]['available'] == "False":
            status = "SOLD"
        elif players_list[i]['seller_id'] == vars.user_id and expire_date > datetime.now() and players_list[i]['available'] == "True":
            status = "ACTIVE"
        elif players_list[i]['seller_id'] == vars.user_id and expire_date < datetime.now() and players_list[i]['available'] == "True":
            status = "EXPIRED"
        # elif players_list[i]['seller_id'] != vars.user_id and players_list[i]['available'] == "False":
        else:
            status = "BOUGHT"

        if players_list[i]['position'] == "GK":
            attributes = [status,
                          players_list[i]['price'],
                          color + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['revision'],
                          players_list[i]['gk_diving'],
                          players_list[i]['gk_handling'],
                          players_list[i]['gk_kicking'],
                          players_list[i]['gk_reflexes'],
                          players_list[i]['gk_speed'],
                          players_list[i]['gk_positoning'] + Bcolors.ENDC]
        else:
            attributes = [status,
                          players_list[i]['price'],
                          color + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['revision'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'] + Bcolors.ENDC]

        spreadsheet.add_row(attributes)

    print(spreadsheet)


def main_menu_menupoints():
    print(30 * "-", "FUT MENU", 30 * "-")
    print("1. SELL player from Reserve Team ")
    print("2. BUY player from Market ")
    print("3. List buy/sell history ")
    print("4. Search for player ")
    print("5. My Team ")
    print("6. Log out ")
    print(70 * "-")
    print()


def my_team_menupoints():
    print(28 * "-", "TEAM EDITOR", 29 * "-")
    print("  1. Show Starting 11")
    print("  2. Show Reserve Team")
    print("  3. Edit My Team")
    print(70 * "-")


def player_search_menupoints():
    print(28 * "-", "PLAYER SEARCH", 27 * "-")
    print("  1. Name")
    print("  2. Quality")
    print("  3. Position")
    print("  4. Country")
    print("  5. Club")
    print("  6. Rarity")
    print("  7. League")
    print("  8. Overall rating")
    print(70 * "-")


def market_search_menupoints():
    print(28 * "-", "MARKET SEARCH", 27 * "-")
    print("  1.  Name")
    print("  2.  Quality")
    print("  3.  Position")
    print("  4.  Country")
    print("  5.  Club")
    print("  6.  Rarity")
    print("  7.  League")
    print("  8.  Overall rating")
    print("  9.  Min price")
    print("  10. Max price")
    print(70 * "-")
