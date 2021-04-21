from daos.account_dao import AccountDAO
from daos.client_dao_impl import ClientDAOImpl
from exceptions.resource_not_found import ResourceNotFound
from models.account import Account
from util.db_connection import connection


class AccountDAOImpl(AccountDAO):
    def create_account(self, account, client_id):
        # Check that the client exists; raise 404 if not
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(client_id)
        except ResourceNotFound as r:
            raise r

        sql = "INSERT INTO accounts VALUES (DEFAULT,%s,0) RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, [client_id])

        connection.commit()
        rec = cursor.fetchone()

        new_account = Account(rec[0], rec[1]).json()
        return new_account

    def all_accounts(self, client_id):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(client_id)
        except ResourceNotFound as r:
            raise r

        sql = "SELECT * FROM accounts WHERE client_id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        rec = cursor.fetchall()

        acc_list = []
        for r in rec:
            record = Account(r[0], r[1], r[2])
            acc_list.append(record.json())
        return acc_list

    def get_account(self, client_id, account_id):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(client_id)
        except ResourceNotFound as r:
            raise r

        sql = "SELECT * FROM accounts WHERE client_id = %s AND account_id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, (client_id, account_id))
        rec = cursor.fetchone()

        if rec:
            account = Account(rec[0], rec[1], rec[2])
            return account
        else:
            raise ResourceNotFound(f"Account {account_id} not found for client {client_id}")

    def get_bounds(self, client_id, low_bound, high_bound):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(client_id)
        except ResourceNotFound as r:
            raise r

        sql = "SELECT * FROM accounts WHERE client_id = %s AND saved >= %s AND saved <= %s"

        cursor = connection.cursor()
        cursor.execute(sql, (client_id, low_bound, high_bound))
        rec = cursor.fetchall()

        acc_list = []
        for r in rec:
            record = Account(r[0], r[1], r[2])
            acc_list.append(record.json())
        return acc_list

    def update_account(self, change):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(change.client_id)
        except ResourceNotFound as r:
            raise r
        try:
            self.get_account(change.client_id, change.account_id)
        except ResourceNotFound as r:
            raise r

        sql = "UPDATE accounts SET client_id=%s, saved=%s WHERE account_id=%s RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (change.client_id, change.saved, change.account_id))
        connection.commit()
        return ''

    def delete_account(self, client_id, account_id):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(client_id)
        except ResourceNotFound as r:
            raise r
        try:
            self.get_account(client_id, account_id)
        except ResourceNotFound as r:
            raise r

        sql = "DELETE FROM accounts WHERE account_id = %s RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, account_id)
        connection.commit()
        return ''
