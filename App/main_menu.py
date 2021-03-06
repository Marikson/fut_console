import display
import sell
import player_search
import team_editor
import market_checker



def get_menu_choice():
    loop = True
    while loop:
        display.main_menu_menupoints()
        choice = input("Enter your choice: ")
        if choice == '1':
            sell.sell_player()
        elif choice == '2':
            player_search.search_for_player(True)
        elif choice == '3':
            market_checker.market_check()
        elif choice == '4':
            player_search.search_for_player()
        elif choice == '5':
            team_editor.my_team()
        elif choice == '6':
            print("Logging out..." + '\n')
            return
        else:
            display.print_warning("Wrong menu selection. Enter any key to try again..")