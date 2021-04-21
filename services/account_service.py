from flask import jsonify

from daos.account_dao_impl import AccountDAOImpl
from exceptions.insufficient_funds import InsufficientFunds


class AccountService:
    account_dao = AccountDAOImpl()

    @classmethod
    def create_account(cls, account, client_id):
        return cls.account_dao.create_account(account, client_id)

    @classmethod
    def all_accounts(cls, client_id):
        return cls.account_dao.all_accounts(client_id)

    @classmethod
    def get_account(cls, client_id, account_id):
        return cls.account_dao.get_account(client_id, account_id)

    @classmethod
    def get_bounds(cls, client_id, low_bound, high_bound):
        accounts = cls.all_accounts(client_id)

        refined_search = []

        for acc in accounts:
            print(acc["saved"])
            if low_bound <= int(acc["saved"]) <= high_bound:
                refined_search.append(acc)

        return refined_search

    @classmethod
    def update_account(cls, change):
        return cls.account_dao.update_account(change)

    @classmethod
    def delete_account(cls, client_id, account_id):
        return cls.account_dao.delete_account(client_id, account_id)

    @classmethod
    def add_funds(cls, client_id, account_id, amount):
        account = cls.account_dao.get_account(client_id, account_id)
        account.saved += amount
        cls.update_account(account)
        return jsonify(account.json())

    @classmethod
    def remove_funds(cls, client_id, account_id, amount):
        account = cls.account_dao.get_account(client_id, account_id)
        if account.saved >= amount:
            account.saved -= amount
            cls.update_account(account)
            return jsonify(account.json())
        else:
            raise InsufficientFunds("Insufficient Funds")

    @classmethod
    def transfer_funds(cls, client_id, account_id, dest_id, amount):
        try:
            cls.remove_funds(client_id, account_id, amount)
            return cls.add_funds(client_id, dest_id, amount)
        except InsufficientFunds as f:
            raise f
