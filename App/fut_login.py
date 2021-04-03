import sys
import requests
import fut_display


credentials_URL = 'http://localhost:3000/Credentials'
user_id = None
login_tries = 1


def try_log_in(tries):
    # if True:
    if log_in(tries):
        fut_display.get_menu_choice()
    else:
        try_log_in(tries + 1)


def log_in(tries):
    if tries > 3:
        sys.exit("Sorry, you are unable to log in!")
    else:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        return authenticate(username, password)


def authenticate(usern, pw):
    try:
        response = requests.get(credentials_URL, {'name': usern})
        user = response.json()
        if user:
            if user[0]['password'] == pw:
                print('\n' + fut_display.Bcolors.OKBLUE + "Hello " + usern + "!" + fut_display.Bcolors.ENDC + '\n')
                global user_id
                user_id = user[0]['id']
                return True

        print(fut_display.Bcolors.WARNING + "Wrong username, or password!" + fut_display.Bcolors.ENDC)
        print()
        return False
    except requests.exceptions.Timeout as errt:
        print(fut_display.Bcolors.WARNING + "Timeout Error:" + fut_display.Bcolors.ENDC, errt)
        return False
    except requests.exceptions.TooManyRedirects as errw:
        print(fut_display.Bcolors.WARNING + "Wrong URL:" + fut_display.Bcolors.ENDC, errw)
        return False
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    except ValueError:
        print(fut_display.Bcolors.WARNING + "No JSON returned!" + fut_display.Bcolors.ENDC)
        return False
