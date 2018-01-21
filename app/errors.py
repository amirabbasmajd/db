from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@error.app_errorhandler(500)
def internal_server(e):
    return render_template('errors/500.html'), 500


@error.app_errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@error.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403
