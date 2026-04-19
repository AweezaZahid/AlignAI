from flask import Flask
from flask_cors import CORS
from database import init_db
from auth import auth

app = Flask(__name__)
CORS(app)  # Allows your HTML files to talk to Flask

app.register_blueprint(auth)

init_db()  # Creates alignai.db and users table on startup

if __name__ == '__main__':
    app.run(debug=True)