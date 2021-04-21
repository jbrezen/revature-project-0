from daos.client_dao import ClientDAO
from exceptions.resource_not_found import ResourceNotFound
from models.client import Client
from util.db_connection import connection


class ClientDAOImpl(ClientDAO):
    def create_client(self, client):
        sql = "INSERT INTO clients VALUES (DEFAULT,%s,%s,%s) RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (client.first_name, client.last_name, client.pin))

        connection.commit()
        rec = cursor.fetchone()

        new_client = Client(rec[0], rec[1], rec[2], rec[3]).json()
        return new_client

    def get_client(self, client_id):
        sql = "SELECT * FROM clients WHERE client_id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        rec = cursor.fetchone()

        if rec:
            client = Client(rec[0], rec[1], rec[2], rec[3])
            return client
        else:
            raise ResourceNotFound("Client ID not found")

    def all_clients(self):
        sql = "SELECT * FROM clients"

        cursor = connection.cursor()
        cursor.execute(sql)
        rec = cursor.fetchall()

        client_list = []
        for r in rec:
            record = Client(r[0], r[1], r[2], r[3])
            client_list.append(record.json())
        return client_list

    def update_client(self, change):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(change.client_id)
        except ResourceNotFound as r:
            raise r

        sql = "UPDATE clients SET first_name=%s, last_name=%s, pin=%s WHERE client_id=%s RETURNING *"

        cursor = connection.cursor()
        cursor.execute(sql, (change.first_name, change.last_name, change.pin, change.client_id))
        connection.commit()
        return ''

    def delete_client(self, client_id):
        try:
            temp_dao = ClientDAOImpl()
            temp_dao.get_client(client_id)
        except ResourceNotFound as r:
            raise r

        sql = "DELETE FROM clients WHERE client_id=%s"

        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()
        return ''
