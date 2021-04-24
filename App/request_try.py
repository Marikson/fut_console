import requests
import display
import json


def try_request_get(url, params):
    try:
        response = requests.get(url, params)
        if response.status_code == 404:
            print(url + display.Bcolors.WARNING + " Not found!" + display.Bcolors.ENDC)
            raise SystemExit()
        json_data = response.json()
        return json_data

    except requests.exceptions.Timeout as errt:
        error_string = "Timeout Error:" + str(errt)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.TooManyRedirects as errw:
        error_string = "Timeout Error:" + str(errw)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.HTTPError as errh:
        error_string = "Timeout Error:" + str(errh)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.ConnectionError as errc:
        error_string = "Timeout Error:" + str(errc)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.RequestException as err:
        error_string = "Timeout Error:" + str(err)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except ValueError:
        print(display.Bcolors.WARNING + "No JSON returned!" + display.Bcolors.ENDC)
        raise SystemExit()


def try_request_patch(url, params):
    param = json.dumps(params)
    try:
        response = requests.patch(url, data=param, headers={"Content-Type": "application/json"})
        if response.status_code == 404:
            print(url + display.Bcolors.WARNING + " Not found!" + display.Bcolors.ENDC)
            return False

        return True
    except requests.exceptions.Timeout as errt:
        error_string = "Timeout Error:" + str(errt)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.TooManyRedirects as errw:
        error_string = "Timeout Error:" + str(errw)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.HTTPError as errh:
        error_string = "Timeout Error:" + str(errh)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.ConnectionError as errc:
        error_string = "Timeout Error:" + str(errc)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.RequestException as err:
        error_string = "Timeout Error:" + str(err)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")


def try_request_post(url, params):
    param = json.dumps(params)
    try:
        response = requests.post(url, data=param, headers={"Content-Type": "application/json"})
        if response.status_code == 404:
            print(url + display.Bcolors.WARNING + " Not found!" + display.Bcolors.ENDC)
            return False

        return True
    except requests.exceptions.Timeout as errt:
        error_string = "Timeout Error:" + str(errt)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.TooManyRedirects as errw:
        error_string = "Timeout Error:" + str(errw)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.HTTPError as errh:
        error_string = "Timeout Error:" + str(errh)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.ConnectionError as errc:
        error_string = "Timeout Error:" + str(errc)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")
    except requests.exceptions.RequestException as err:
        error_string = "Timeout Error:" + str(err)
        display.print_warning(error_string)
        raise SystemExit("Please try again later!")

