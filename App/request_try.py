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
        print(display.Bcolors.WARNING + "Timeout Error:" + display.Bcolors.ENDC, errt)
    except requests.exceptions.TooManyRedirects as errw:
        print(display.Bcolors.WARNING + "Wrong URL:" + display.Bcolors.ENDC, errw)
    except requests.exceptions.HTTPError as errh:
        print(display.Bcolors.WARNING + "Http Error:" + display.Bcolors.ENDC, errh)
    except requests.exceptions.ConnectionError as errc:
        print(display.Bcolors.WARNING + "Error Connecting:" + display.Bcolors.ENDC, errc)
    except requests.exceptions.RequestException as err:
        print(display.Bcolors.WARNING + "OOps: Something Else" + display.Bcolors.ENDC, err)
        raise SystemExit(err)
    except ValueError:
        print(display.Bcolors.WARNING + "No JSON returned!" + display.Bcolors.ENDC)


def try_request_patch(url, params):
    param = json.dumps(params)
    try:
        response = requests.patch(url, data=param, headers={"Content-Type": "application/json"})
        if response.status_code == 404:
            print(url + display.Bcolors.WARNING + " Not found!" + display.Bcolors.ENDC)
            return False

        return True
    except requests.exceptions.Timeout as errt:
        print(display.Bcolors.WARNING + "Timeout Error:" + display.Bcolors.ENDC, errt)
    except requests.exceptions.TooManyRedirects as errw:
        print(display.Bcolors.WARNING + "Wrong URL:" + display.Bcolors.ENDC, errw)
    except requests.exceptions.HTTPError as errh:
        print(display.Bcolors.WARNING + "Http Error:" + display.Bcolors.ENDC, errh)
    except requests.exceptions.ConnectionError as errc:
        print(display.Bcolors.WARNING + "Error Connecting:" + display.Bcolors.ENDC, errc)
    except requests.exceptions.RequestException as err:
        print(display.Bcolors.WARNING + "OOps: Something Else" + display.Bcolors.ENDC, err)
        raise SystemExit(err)


def try_request_post(url, params):
    param = json.dumps(params)
    try:
        response = requests.post(url, data=param, headers={"Content-Type": "application/json"})
        if response.status_code == 404:
            print(url + display.Bcolors.WARNING + " Not found!" + display.Bcolors.ENDC)
            return False

        return True
    except requests.exceptions.Timeout as errt:
        print(display.Bcolors.WARNING + "Timeout Error:" + display.Bcolors.ENDC, errt)
    except requests.exceptions.TooManyRedirects as errw:
        print(display.Bcolors.WARNING + "Wrong URL:" + display.Bcolors.ENDC, errw)
    except requests.exceptions.HTTPError as errh:
        print(display.Bcolors.WARNING + "Http Error:" + display.Bcolors.ENDC, errh)
    except requests.exceptions.ConnectionError as errc:
        print(display.Bcolors.WARNING + "Error Connecting:" + display.Bcolors.ENDC, errc)
    except requests.exceptions.RequestException as err:
        print(display.Bcolors.WARNING + "OOps: Something Else" + display.Bcolors.ENDC, err)
        raise SystemExit(err)