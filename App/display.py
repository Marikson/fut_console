from prettytable import PrettyTable
import termplotlib


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
    UNDERLINE = '\033[4m'


def show_starting_11(players_list, positions):
    player_rows = ["POS", "Name", "Overall rating", "Preferred Position", "Nationality", "Club", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"]
    spreadsheet = PrettyTable(player_rows)
    for j in range(len(positions)):
        for i in range(len(players_list)):
            if players_list[i]['POS'] == positions[j]:
                if players_list[i]['position'] == "GK":
                    attributes = [positions[j],
                                  players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['gk_diving'],
                                  players_list[i]['gk_handling'],
                                  players_list[i]['gk_kicking'],
                                  players_list[i]['gk_reflexes'],
                                  players_list[i]['gk_speed'],
                                  players_list[i]['gk_positoning']]
                elif players_list[i]['revision'] == "CL":
                    attributes = [positions[j],
                                  Bcolors.OKBLUE + players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['pace'],
                                  players_list[i]['shooting'],
                                  players_list[i]['passing'],
                                  players_list[i]['dribbling'],
                                  players_list[i]['defending'],
                                  players_list[i]['physicality'] + Bcolors.ENDC]
                elif players_list[i]['revision'] == "OTW":
                    attributes = [positions[j],
                                  Bcolors.OKGREEN + players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['pace'],
                                  players_list[i]['shooting'],
                                  players_list[i]['passing'],
                                  players_list[i]['dribbling'],
                                  players_list[i]['defending'],
                                  players_list[i]['physicality'] + Bcolors.ENDC]
                elif players_list[i]['revision'] == 'IF':
                    attributes = [positions[j],
                                  Bcolors.MAGENTA + players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['pace'],
                                  players_list[i]['shooting'],
                                  players_list[i]['passing'],
                                  players_list[i]['dribbling'],
                                  players_list[i]['defending'],
                                  players_list[i]['physicality'] + Bcolors.ENDC]
                elif players_list[i]['revision'] == 'Icon':
                    attributes = [positions[j],
                                  Bcolors.WWHITE + players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['pace'],
                                  players_list[i]['shooting'],
                                  players_list[i]['passing'],
                                  players_list[i]['dribbling'],
                                  players_list[i]['defending'],
                                  players_list[i]['physicality'] + Bcolors.ENDC]
                else:
                    attributes = [positions[j],
                                  players_list[i]['player_extended_name'],
                                  players_list[i]['overall'],
                                  players_list[i]['position'],
                                  players_list[i]['nationality'],
                                  players_list[i]['club'],
                                  players_list[i]['pace'],
                                  players_list[i]['shooting'],
                                  players_list[i]['passing'],
                                  players_list[i]['dribbling'],
                                  players_list[i]['defending'],
                                  players_list[i]['physicality']]
                spreadsheet.add_row(attributes)

    print(spreadsheet)


def show_players(players_list):
    player_rows = ["Name", "Overall rating", "Position", "Nationality", "Club", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physicality"]
    spreadsheet = PrettyTable(player_rows)
    for i in range(len(players_list)):
        if players_list[i]['position'] == "GK":
            attributes = [players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['gk_diving'],
                          players_list[i]['gk_handling'],
                          players_list[i]['gk_kicking'],
                          players_list[i]['gk_reflexes'],
                          players_list[i]['gk_speed'],
                          players_list[i]['gk_positoning']]
        elif players_list[i]['revision'] == "CL":
            attributes = [Bcolors.OKBLUE + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'] + Bcolors.ENDC]
        elif players_list[i]['revision'] == "OTW":
            attributes = [Bcolors.OKGREEN + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'] + Bcolors.ENDC]
        elif players_list[i]['revision'] == 'IF':
            attributes = [Bcolors.MAGENTA + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'] + Bcolors.ENDC]
        elif players_list[i]['revision'] == 'Icon':
            attributes = [Bcolors.WWHITE + players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality'] + Bcolors.ENDC]
        else:
            attributes = [players_list[i]['player_extended_name'],
                          players_list[i]['overall'],
                          players_list[i]['position'],
                          players_list[i]['nationality'],
                          players_list[i]['club'],
                          players_list[i]['pace'],
                          players_list[i]['shooting'],
                          players_list[i]['passing'],
                          players_list[i]['dribbling'],
                          players_list[i]['defending'],
                          players_list[i]['physicality']]

        spreadsheet.add_row(attributes)

    print(spreadsheet)


def show_extended_players(players_list):
    main_rows = ["Name", "Overall", "Acceleration", "Sprint speed", "Positioning", "Finishing", "Shot power", "Penalties", "Free kick", "Crossing", "Long pass", "Short passs", "Ball controll", "Reactions", "Interceptions", "Marking", "Strength", "Stamina"]
    spreadsheet = PrettyTable(main_rows)
    for i in range(len(players_list)):
        if players_list[i]['revision'] == "CL":
            attributes = [Bcolors.OKBLUE + players_list[i]['player_extended_name'],
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
        elif players_list[i]['revision'] == "OTW":
            attributes = [Bcolors.OKGREEN + players_list[i]['player_extended_name'],
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
        elif players_list[i]['revision'] == 'IF':
            attributes = [Bcolors.MAGENTA + players_list[i]['player_extended_name'],
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
        elif players_list[i]['revision'] == 'Icon':
            attributes = [Bcolors.WWHITE + players_list[i]['player_extended_name'],
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
        else:
            attributes = [players_list[i]['player_extended_name'],
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
                          players_list[i]['phys_stamina']]

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


def main_menu_menupoints():
    print(30 * "-", "FUT MENU", 30 * "-")
    print("1. SELL player from MySquad ")
    print("2. BUY player from Market ")
    print("3. List buy/sell history ")
    print("4. Search for player ")
    print("5. Edit team ")
    print("6. Log out ")
    print(70 * "-")
    print()


def my_team_menupoints():
    print(28 * "-", "TEAM EDITOR", 29 * "-")
    print("  1. Show starting 11")
    print("  2. List my players")
    print("  3. Edit starting 11")
    print(70 * "-")


def player_search_menupoints():
    print(28 * "-", "PLAYER SEARCH", 27 * "-")
    print("  1. Name")
    print("  2. Quality")
    print("  3. Position")
    print("  4. Nationality")
    print("  5. Club")
    print("  6. Rarity")
    print("  7. League")
    print("  8. Overall rating")
    print(70 * "-")
