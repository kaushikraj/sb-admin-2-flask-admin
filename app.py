import os
from flask import Flask, url_for, redirect, render_template, request, send_from_directory

import flask_admin as admin
import flask_login as login

from views import AdminIndexView, BlankView
from user import User


# = Create Flask application object
#
app = Flask(__name__)


# == Helpers
#
# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


# = Assets routes
#
# bower_components
@app.route('/bower_components/<path:path>')
def send_bower(path):
    return send_from_directory(os.path.join(app.root_path, 'bower_components'), path)

@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory(os.path.join(app.root_path, 'dist'), path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(app.root_path, 'js'), path)

# Flask views
@app.route('/')
def index():
    return render_template("sb-admin/redirect.html")


# == Start the App
#
# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Initialize flask-login
init_login()

# Create admin with flask-admin
admin = admin.Admin(app,
    'SB-Admin-2',
    index_view=AdminIndexView())

# Example how ot add views to the admin
admin.add_view(BlankView(name='Blank', url='blank', endpoint='blank'))

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
    )
