import requests

url = "http://api.airvisual.com/"
payload = {}
headers= {'Content-Type':'application/json'}
apiKey = ""
invalidApiKey = "abcxyz"
status_success = 200
status_forbidden = 403
status_internal_server_error = 500
coordinates = []

with open("ApiKey.txt", 'r') as txtfile:
    for line in txtfile:
        apiKey = line
#     print ("apiKey: {}".format(apiKey))
txtfile.close()

def testAPIAuth():
    """
    Test authentication status
    """
    # Checking 200 status
    url_string = url + "v2/countries?"
    params = {'key': apiKey}
    response = requests.get(url_string, params)
    assert response.status_code == status_success
    print(url_string)
    print("-> Test Valid Auth | Status {}".format(str(response.status_code)))

    # Checking 403 status
    params = {'key': invalidApiKey}
    response = requests.get(url_string, params)
    assert response.status_code == status_forbidden
    print("-> Test Invalid Auth | Status {} \n".format(str(response.status_code)))

def testListStatesAPI():
    """
    list states of a country
    """
    country = "Australia"
    au_states = ['New South Wales', 'Queensland', 'South Australia', 'Tasmania', 'Victoria', 'Western Australia']
    url_string = url + "v2/states?"
    params = {'country': country,
              'key': apiKey}
    response = requests.get(url_string, params)
    assert response.status_code == status_success
    response_body = response.json()
    resp_states = [str(i['state']) for i in response_body["data"]]
    print(url_string)
    print("-> Test List States | Status {}".format(str(response.status_code)))
    print("-> {} : {} \n".format(country, str(resp_states)))
    if 'Australia' in country:
        assert au_states == resp_states

def testNearestCityDataAPI():
    """
    Get nearest city data
    """
    # By IP Geolocation
    global coordinates
    url_string = url + "v2/nearest_city?"
    params = {'key': apiKey}
    response = requests.get(url_string, params)
    assert response.status_code == status_success
    response_body = response.json()
    city = str(response_body["data"]["city"])
    coordinates = str(response_body["data"]["location"]["coordinates"])
    print(url_string)
    print("-> Test Nearest City Data | Status " + str(response.status_code))
    print("-> {} : {} \n".format(city, coordinates))

    # By City GPS coordinates
    coord = [144.771715, -37.8537]
    params = {'lat': str(coord[1]),
              'lon': str(coord[0]),
              'key': apiKey}
    response = requests.get(url_string, params)
    assert response.status_code == status_success
    response_body = response.json()
    city = str(response_body["data"]["city"])
    print("-> Test Another City Data | Status " + str(response.status_code))
    print("-> {} : {} \n".format(city, str(response_body["data"])))

def testGetCityTemperatureAPI(coordinates):
    """
    Get nearest city temperature
    param: coordinates[long, lat] of the city
    """
#     latitude, longitude = '-37.8537', '144.771715'
    latitude, longitude = coordinates[0], coordinates[1]
    url_string = url + "v2/nearest_city?lat="+str(latitude)+"&lon="+str(longitude)+"&key="+apiKey
    response = requests.request("GET", url_string, headers=headers, data = payload)
    assert response.status_code == status_success
    response_body = response.json()
    # print(jsonschema.validate(instance=response_body, schema=json_schema))
    print("-> Test Get Nearest City Temperature | Status " + str(response.status_code))
    print("-> {}: {}\xb0C".format(str(response_body["data"]["city"]), 
                          str(response_body["data"]["current"]["weather"]["tp"])))

if __name__ == "__main__":
    print("Executing Airvisual API tests...")
    testAPIAuth()
    testListStatesAPI()
    testNearestCityDataAPI()
    testGetCityTemperatureAPI(coordinates)
