from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from geocodio import GeocodioClient
from pyzomato import Pyzomato
import requests
import json

#Flask app setup
app = Flask(__name__)
app.secret_key = 'Secret Key'

#API keys
zKey = '3637e5d5a1b6d7c7ab4aae535a508b13'
geoKey = '7dff5f5b70e753fe777774b74004fb73e3f3037'

zClient = Pyzomato(zKey)
geoClient = GeocodioClient(geoKey)


@app.route('/', methods=["POST", "GET"])
def homePage():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        address = request.form['address']
        try:
            location = geoClient.geocode(address)
            return getRestaurants(address)
        except:
            flash('Please enter a valid address')
            return redirect('/')


def getRestaurants(address):
    location = geoClient.geocode(address)

    loc = json.dumps(location)

    locDict = json.loads(loc)

    lat = locDict['results'][0]['location']['lat']
    lon = locDict['results'][0]['location']['lng']

    data = zClient.getByGeocode(lat, lon)

    restaurantData = data['nearby_restaurants']

    output = list()
    for restaurant in restaurantData:
        tmp = dict()
        tmp['name'] = restaurant['restaurant']['name']
        tmp['address'] = restaurant['restaurant']['location']['address']
        tmp['cuisines'] = restaurant['restaurant']['cuisines']
        tmp['rating'] = restaurant['restaurant']['user_rating']['aggregate_rating']
        output.append(tmp)
    return jsonify(output)
