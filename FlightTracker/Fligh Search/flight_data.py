import json
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.flights = {}
        self.price = 0
    
    def flights_filter(self, ddt):
        try:
            for key in ddt:
                flights = {
                    "price" : key["price"]["total"],
                    "destination" : key["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
                    "class" : key["travelerPricings"][0]["fareDetailsBySegment"][0]["cabin"]
                    }
                self.flights[key["id"]] = flights
            return self.flights
        except:
            flights = {
                "price" : 0,
                "destination" : "null",
                "class" : "null"
                }
            self.flights[key["id"]] = flights
            return self.flights
