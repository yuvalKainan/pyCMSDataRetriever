import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import json

import numpy


def getDataFromCMS(countryCode,destCode):
    session = requests.session
    payload = {'name': '',
               'email': 'admin@routeperfect.com',
               'pass': '123456789'}
    loginURL = "https://cms.routeperfect.com/actions/login.php"
    getURL = "https://cms.routeperfect.com/scores.php?country=" + str(countryCode) + "&place=" + str(destCode)
    with requests.Session() as s:
        p = s.post(loginURL, data=payload)
        r = s.get(getURL)
    return r.text

def loadCities():
    json1_file = open('cities.json')
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    cities = {}
    for dataPoint in json1_data:
        cities[dataPoint['name']] = [dataPoint['country_id'],dataPoint['place_id']]
    return cities

def getScores(cityName):
    cities = loadCities()
    countryCode,placeCode = cities[cityName]
    print("countryCode = " + str(countryCode))
    print("placeCode = " + str(placeCode))
    data = getDataFromCMS(countryCode,placeCode)
    soup = bs(data,  "html.parser")
    txt = soup.__unicode__()
    scores = txt.split('</dl>')
    dict = {}
    dict['nights'] = scores[2].split('nights')[1].split('value=')[1].split('/>')[0]
    scores = scores[3:15]
    dict['romantic'] = scores[8].split('value=')[1].split('/>')[0]
    dict['friends'] = scores[9].split('value=')[1].split('/>')[0]
    dict['family'] = scores[10].split('value=')[1].split('/>')[0]
    dict['other'] = scores[11].split('value=')[1].split('/>')[0]
    dict['smallTown'] = scores[0].split('value=')[1].split('/>')[0]
    dict['colture'] = scores[1].split('value=')[1].split('/>')[0]
    dict['food'] = scores[2].split('value=')[1].split('/>')[0]
    dict['nature'] = scores[3].split('value=')[1].split('/>')[0]
    dict['historic'] = scores[4].split('value=')[1].split('/>')[0]
    dict['beaches'] = scores[5].split('value=')[1].split('/>')[0]
    dict['nightLife'] = scores[6].split('value=')[1].split('/>')[0]
    dict['active'] = scores[7].split('value=')[1].split('/>')[0]
    return dict

def main(cityName):
    dict = getScores(cityName)
    for i in dict:
        print(i +" "+ dict[i].split('"')[1].split('"')[0])

while True:
    print('***********************************************************************************************')
    print("Enter Destination name:")
    cityName = input()
    try:
        main(cityName)
    except:
        print('misspell? did you use Capitalization?')