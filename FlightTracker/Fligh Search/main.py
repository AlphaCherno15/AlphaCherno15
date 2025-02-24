#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import flight_search, data_manager, time, datetime as dt, notification_manager, flight_data


fs = flight_search.FlightSearch()
fs_dt = flight_data.FlightData()
dm = data_manager.DataManager()
sms = notification_manager.NotificationManager()
sheet_data = dm.read()

for airport in sheet_data:
    if airport["iataCode"] == "":
        dm.edit(fs.airport("Testing"),airport["id"]) 
def main():
    for destin in sheet_data:
        IATA = fs.airport(destin["city"])
        flight_list = fs.get_flight(IATA, "2025-01-25", origin="LON")
        price_list = [float(value["price"]) for value in fs_dt.flights_filter(flight_list).values()]
        lowest_price = min(price_list)
        sheet_id = destin["id"]
        if lowest_price < float(destin["lowestPrice"]):
            dm.edit(IATA, lowest_price, sheet_id)
            try:
                sms.send(f"Lowest price for {destin['city']} is {lowest_price}")
            except:
                print("SMS NOT WORKING")
            time.sleep(2)
IATA = fs.airport("toronto")
flight_list = fs.get_flight(IATA, "2025-01-25", origin="YYG")
flights = fs_dt.flights_filter(flight_list)
print(flights.values())