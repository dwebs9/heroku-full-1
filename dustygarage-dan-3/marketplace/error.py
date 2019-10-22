from flask import render_template
from . import db, create_app


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html'), 404
