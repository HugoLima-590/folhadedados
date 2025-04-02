from flask import Flask
from flask_cors import CORS
from server.routes.process import process_blueprint
from server.routes.download import download_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(process_blueprint)
app.register_blueprint(download_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)