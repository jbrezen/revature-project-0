from exceptions.resource_not_found import ResourceNotFound
from models.client import Client
from services.client_service import ClientService
from flask import request, jsonify


def route(app):
    # Create a new client
    @app.route("/clients/", methods=['POST'])
    def post_client():
        client = Client.json_parse(request.json)
        ClientService.create_client(client)
        return jsonify(client.json()), 201

    # Get a list of all clients
    @app.route("/clients/", methods=['GET'])
    def all_clients():
        return jsonify(ClientService.all_clients()), 200

    # Get a single client by ID
    @app.route("/clients/<client_id>/", methods=['GET'])
    def get_client(client_id):
        try:
            client = ClientService.get_client(client_id)
            return jsonify(client.json()), 200
        except ValueError as e:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404

    # Put an existing client object with the given ID
    @app.route("/clients/<client_id>/", methods=['PUT'])
    def put_client(client_id):
        try:
            client = Client.json_parse(request.json)
            client.client_id = int(client_id)
            ClientService.update_client(client)
            return jsonify(client.json()), 200
        except ResourceNotFound as r:
            return r.message, 404

    # Delete a client by ID
    @app.route("/clients/<client_id>/", methods=['DELETE'])
    def delete_client(client_id):
        try:
            ClientService.delete_client(client_id)
            return '', 204
        except ValueError:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404
