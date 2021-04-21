class Client:

    def __init__(self, client_id=0, first_name='', last_name='', pin=''):
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin

    def json(self):
        return {
            'clientID': self.client_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'pin': self.pin,
        }

    @staticmethod
    def json_parse(json):
        client = Client()
        client.client_id = json['clientID'] if 'clientID' in json else 0
        client.first_name = json['firstName']
        client.last_name = json['lastName']
        client.pin = json['pin']
        return client

    def __repr__(self):
        return str(self.json())
