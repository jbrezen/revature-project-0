class Account:

    def __init__(self, account_id=0, client_id=0, saved=0):
        self.account_id = account_id
        self.client_id = client_id
        self.saved = saved

    def deposit(self, amount=0):
        if amount >= 0:
            self.saved += amount
        else:
            return -1

    def withdraw(self, amount=0):
        if amount >= 0:
            if self.saved >= amount:
                self.saved -= amount
            else:
                return -2
        else:
            return -1

    def json(self):
        return {
            'accountID': self.account_id,
            'clientID': self.client_id,
            'saved': self.saved
        }

    @staticmethod
    def json_parse(json):
        account = Account()
        account.account_id = json['accountID']
        account.client_id = json['clientID']
        account.saved = json['saved']
        return account
