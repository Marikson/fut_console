import sys
import display
import main_menu
import request_try
import vars

login_tries = 1


def try_log_in(tries):
    if log_in(tries):
        main_menu.get_menu_choice()
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
            greeting = "Hello " + usern + "!"
            display.print_info(greeting)
            user_id = user[0]['id']
            users_id_url = vars.users_URL + '/' + str(user_id)
            vars.set_user_vars(users_id_url, user_id)
            return True

    display.print_warning("Wrong username, or password!")
    return False

