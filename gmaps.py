from flask import json
import requests
from urllib import quote

__author__ = 'JP'


API_DIRECTION_BASE = 'https://maps.googleapis.com/maps/api/directions/json?'

API_KEY = 'AIzaSyBp101OIf6PY_kSb24KfqTFFZIcixmbQuI'


def getDirections(origin,destination):
    direction_search_result = requests.get("{}&origin={}&destination={}&key={}".format(
        API_DIRECTION_BASE,
        origin,
        destination,
        API_KEY
    )).json()

    route_steps = direction_search_result[] 




'''

from flask import json
import requests
from urllib import quote

__author__ = 'Laura'

API_WIKIPEDIA_BASE = 'http://en.wikipedia.org/w/api.php?action=query'

## http://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=Threadless&format=json&exintro=1

def wikipediasearch(text):
    wikipedia_search_result = requests.get("{}&prop={}&titles={}&format={}&exintro={}".format(
        API_WIKIPEDIA_BASE,
        'info',
        quote(text),
        'json',
        0
    )).json()

    page_id = wikipedia_search_result['query']['pages'].values()[0]['pageid']

    wikipedia_url = requests.get("http://en.wikipedia.org/w/api.php?action=query&prop=info&pageids={}&inprop=url&format=json".format(
                                 page_id)).json()


    return json.jsonify(url=wikipedia_url['query']['pages'].values()[0]['fullurl'])


##    wikipedia_search_result = requests.get("{}&prop={}&titles={}&rvprop={}&format={}&rvsection={}&rvparse={}".format(
##        API_WIKIPEDIA_BASE,
##        'revisions',
##        quote(text),
##       'content',
##        'json',
##        0,
##        1
##    )).json()

'''