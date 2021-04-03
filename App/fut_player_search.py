import requests
import fut_display
import fut_vars


def search_for_player():
    print(28 * "-", "PLAYER SEARCH", 27 * "-")
    params = {}
    print("  1. Name")
    print("  2. Quality")
    print("  3. Position")
    print("  4. Nationality")
    print("  5. Club")
    print("  6. Rarity")
    print("  7. League")
    print("  8. Overall rating")
    # print("  9. Back")
    print(70 * "-")
    input_nums = input("  Enter aspect(s)(separated by space) you want to filter by: ")
    nums_list = input_nums.split()
    for i in range(len(nums_list)):
        try:
            if nums_list[i] == "back":
                print(fut_display.Bcolors.OKBLUE + "  Going back to FUT MENU" + fut_display.Bcolors.ENDC + '\n')
                fut_display.get_menu_choice()
            elif int(nums_list[i]) > 8 or int(nums_list[i]) < 1:
                print(fut_display.Bcolors.WARNING + "  No aspect found with number: " + nums_list[i] + "!" + fut_display.Bcolors.ENDC)
                search_for_player()

        except ValueError:
            print(fut_display.Bcolors.WARNING + "  Aspect input must be a number! Given '" + nums_list[i] + "' is wrong." + fut_display.Bcolors.ENDC)
            search_for_player()

    for i in range(len(nums_list)):
        given_val = input("      Enter " + fut_vars.search_aspect[int(nums_list[i]) - 1] + ": ")
        if given_val == 'back':
            search_for_player()
        else:
            params[ fut_vars.search_aspect[int(nums_list[i]) - 1] ] = given_val

    try:
        response = requests.get(fut_vars.players_URL, params)
        matched_players = response.json()
        if matched_players:
            fut_display.show_players(matched_players)
        else:
            print(fut_display.Bcolors.OKCYAN + "No matching player with params above!" + fut_display.Bcolors.ENDC + '\n')
    except requests.exceptions.Timeout as errt:
        print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
    except requests.exceptions.TooManyRedirects as errw:
        print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    except ValueError:
        print(fut_display.Bcolors.WARNING + "No JSON returned!" + fut_display.Bcolors.ENDC)

    fut_display.get_menu_choice()