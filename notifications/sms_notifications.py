from twilio.rest import Client

class SMSNotifier:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, to_number, from_number, message):
        self.client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
