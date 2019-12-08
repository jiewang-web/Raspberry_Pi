import requests
import json

appid = "fcb16e9d9981546e6c11f8f494e6fdc9"
func = "forecast"
loc = "63112,us"

def weatherurlbuilder(function=func, location=loc, key=appid):
    """
    :param function: weather/ forecast / somewhat
    :param location: zip code + country
    :param key: Key
    :return: url for request GET
    """
    url = "http://api.openweathermap.org/data/2.5/{}?zip={}&APPID={}"
    return url.format(function, location, key)
