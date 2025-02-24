import requests as rq, json, os
from dotenv import load_dotenv
load_dotenv()

# https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["amadeus_api_key"]
        self._api_secret = os.environ["amadeus_api_secret"]
        self.endpoint = "https://test.api.amadeus.com/v1"
        self._token = self._get_token()
        self._bearer_headers = {
            "Authorization": f"Bearer {self._token}"
        }
    def _get_token(self):
        param = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        head = {"content-type":"application/x-www-form-urlencoded"}
        token = rq.post(f'{self.endpoint}/security/oauth2/token', data=param, headers=head)
        return token.json()["access_token"]

    def airport(self, city):
        param = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS"
        }
        request = rq.get(f'{self.endpoint}/reference-data/locations/cities', params=param, headers=self._bearer_headers)
        response = request.json()
        try:
            iata = response["data"][0]["iataCode"]
        except IndexError:
            return "N/A"
        except KeyError:
            return "Not Found"
        return iata
    def get_flight(self, destination, departure, adults=1, origin="YYG", currency="CAD",**kwargs):
        return_date = kwargs.get("return")
        travel_class = kwargs.get("class")
        non_stop = kwargs.get("non_stop")
        endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        param = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure,
            "returnDate": return_date,
            "adults": adults,
            "nonStop": non_stop, #true or false
            "travelClass": travel_class, #ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
            "currencyCode": currency
        }
        request = rq.get(endpoint, params=param, headers=self._bearer_headers)
        response = request.json()
        with open(f"Fligh Search/flight_data.json", "w") as file:
            json.dump(response["data"], file, indent=4)
        return response["data"]
# test = FlightSearch()
# print(test.get_flight(destination="YYG", departure="2025-01-25", origin="LON", non_stop="true", travel_class="ECONOMY"))
