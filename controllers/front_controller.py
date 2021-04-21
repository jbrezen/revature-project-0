from controllers import client_controller, account_controller


def route(app):
    client_controller.route(app)
    account_controller.route(app)