from flask import request, jsonify
from werkzeug.exceptions import abort

from exceptions.insufficient_funds import InsufficientFunds
from exceptions.resource_not_found import ResourceNotFound
from models.account import Account
from services.account_service import AccountService


def route(app):
    # Create a new account for the given client
    @app.route("/clients/<client_id>/accounts", methods=['POST'])
    def post_account(client_id):
        try:
            account = Account.json_parse(request.json)
            AccountService.create_account(account, client_id)
            return jsonify(account.json()), 201
        except ResourceNotFound as r:
            return r.message, 404

    # Get all accounts from a given client
    @app.route("/clients/<client_id>/accounts", methods=['GET'])
    def all_accounts(client_id):
        try:
            return jsonify(AccountService.all_accounts(client_id)), 200
        except ResourceNotFound as r:
            return r.message, 404

    # Get accounts with funds between given bounds
    @app.route("/clients/<client_id>/accounts", methods=['GET'])
    def get_bounds(client_id):
        high_bound = request.args.get("amountLessThan")
        low_bound = request.args.get("amountGreaterThan")
        try:
            return jsonify(AccountService.get_bounds(client_id, low_bound, high_bound)), 200
        except ResourceNotFound as r:
            return r.message, 404

    # Get a single account from this client by ID
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['GET'])
    def get_account(client_id, account_id):
        try:
            account = AccountService.get_account(client_id, account_id)
            return jsonify(account.json()), 200
        except ValueError as e:
            return "Invalid ID", 400
        except ResourceNotFound as r:
            return r.message, 404

    # Put an account object with the given ID
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['PUT'])
    def put_account(client_id, account_id):
        try:
            account = Account.json_parse(request.json)
            account.account_id = int(account_id)
            account.client_id = int(client_id)
            AccountService.update_account(account)
            return jsonify(account.json()), 200
        except ValueError as e:
            return "Incorrect Value Type", 400
        except ResourceNotFound as r:
            return r.message, 404

    # Delete an account from this client by ID
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['DELETE'])
    def delete_account(client_id, account_id):
        try:
            AccountService.delete_account(client_id, account_id)
            return '', 204
        except ValueError as e:
            return "Incorrect value type", 400
        except ResourceNotFound as r:
            return r.message, 404

    # Make a deposit or withdrawal
    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['PATCH'])
    def patch_account(client_id, account_id):
        is_withdraw = 'withdraw' in request.json
        is_deposit = 'deposit' in request.json

        if is_withdraw:
            amount = request.json['withdraw']
            try:
                AccountService.remove_funds(client_id, account_id, amount)
                return f"Successfully withdrew {amount} from account {account_id}", 200
            except ValueError as e:
                return "Incorrect Value Type", 400
            except InsufficientFunds as f:
                return f.message, 422
            except ResourceNotFound as r:
                return r.message, 404
        elif is_deposit:
            amount = request.json['deposit']
            try:
                AccountService.add_funds(client_id, account_id, amount)
                return f"Successfully deposited {amount} into account {account_id}", 200
            except ValueError as e:
                return "Incorrect Value Type", 400
            except ResourceNotFound as r:
                return r.message, 404
        else:
            abort(400, "Body must contain a JSON with either a 'withdraw' or 'deposit' property")

    @app.route("/clients/<client_id>/accounts/<account_id>/transfer/<dest_id>", methods=['PATCH'])
    def transfer_funds(client_id, account_id, dest_id):
        if "amount" in request.json:
            amount = request.json["amount"]
            try:
                AccountService.transfer_funds(client_id, account_id, dest_id, amount)
                return f"Successfully transferred ${amount} from account {account_id} to {dest_id}", 200
            except ValueError as e:
                return "Incorrect Value Type", 400
            except ResourceNotFound as r:
                return r.message, 404
            except InsufficientFunds as f:
                return f.message, 422
        else:
            abort(400, "Body must contain a JSON with an 'amount' property")
