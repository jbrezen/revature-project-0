from abc import ABC, abstractmethod


class AccountDAO(ABC):

    @abstractmethod
    def create_account(self, account, client_id):
        pass

    @abstractmethod
    def all_accounts(self, client_id):
        pass

    @abstractmethod
    def get_account(self, client_id, account_id):
        pass

    @abstractmethod
    def get_bounds(self, client_id, low_bound, high_bound):
        pass

    @abstractmethod
    def update_account(self, change):
        pass

    @abstractmethod
    def delete_account(self, account_id):
        pass
