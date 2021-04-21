from daos.client_dao_impl import ClientDAOImpl


class ClientService:
    client_dao = ClientDAOImpl()

    @classmethod
    def create_client(cls, client):
        return cls.client_dao.create_client(client)

    @classmethod
    def get_client(cls, client_id):
        return cls.client_dao.get_client(client_id)

    @classmethod
    def all_clients(cls):
        return cls.client_dao.all_clients()

    @classmethod
    def update_client(cls, change):
        return cls.client_dao.update_client(change)

    @classmethod
    def delete_client(cls, client_id):
        return cls.client_dao.delete_client(client_id)
