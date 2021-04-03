from prettytable import PrettyTable
import fut_player_search
import fut_team_editor
import fut_login


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_menu_choice():
    loop = True
    while loop:
        print(30 * "-", "FUT MENU", 30 * "-")
        print("1. SELL player from MySquad ")
        print("2. BUY player from Market ")
        print("3. List buy/sell history ")
        print("4. Search for player ")
        print("5. Edit team ")
        print("6. Log out ")
        print(70 * "-")
        print()
        choice = input("Enter your choice: ")

        if choice == '1':
            loop = False
        elif choice == '2':
            loop = False
        elif choice == '3':
            loop = False
        elif choice == '4':
            fut_player_search.search_for_player()
            loop = False
        elif choice == '5':
            fut_team_editor.my_team()
            # starting_eleven()
            loop = False
        elif choice == '6':
            print("Logging out..." + '\n')
            fut_login.try_log_in(fut_login.login_tries)
            loop = False
        else:
            input(Bcolors.WARNING + "Wrong menu selection. Enter any key to try again.." + Bcolors.ENDC)


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