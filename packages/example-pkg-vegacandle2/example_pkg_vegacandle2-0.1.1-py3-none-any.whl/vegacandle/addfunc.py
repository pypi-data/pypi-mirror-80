import requests

VERSION = "2.2.2"

def getMyIP():
    url = "https://api.ipify.org?format=json"
    response = requests.get(url)
    return response.json()


def getIPInfo(ip):
    url = "http://ip-api.com/json/{}".format(ip)
    response = requests.get(url)
    return response.json()

def add(a,b):
    city = getIPInfo(getMyIP()["ip"])["city"]
    msg = "You're in {}. Do you want make {} + {} right? This is version {}".format(city, a, b, VERSION)
    print(msg)
    return msg

# add(4,5)