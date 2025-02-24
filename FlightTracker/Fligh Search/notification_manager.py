from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self._account_sid = ""
        self._auth_token = ""
        self.number = ""
    def send(self, destination, price):
        client = Client(self._account_sid, self._auth_token)
        message = client.messages.create(
            from_="+xxxx",
            body=f"It was found that the flight to {destination} is cheaper, the new price is {price}",
            to= self.number
        )