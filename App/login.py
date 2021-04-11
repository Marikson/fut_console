import sys
import display
import request_try
import vars

user_id = None
login_tries = 1


def try_log_in(tries):
    # if True:
    if log_in(tries):
        display.get_menu_choice()
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
    user = request_try.try_request_get(vars.credentials_URL, {'name': usern})
    if user:
        if user[0]['password'] == pw:
            print('\n' + display.Bcolors.OKBLUE + "Hello " + usern + "!" + display.Bcolors.ENDC + '\n')
            global user_id
            user_id = user[0]['id']
            return True

    print(display.Bcolors.WARNING + "Wrong username, or password!" + display.Bcolors.ENDC)
    print()
    return False

