from flask import Flask
from flask_cors import CORS

from ebay import ebay

app = Flask(__name__)

CORS(app)

@app.route("/api")
def index():
    return

@app.route("/api/callback", methods=['GET', 'POST'])
def callback():
    return ebay.callback_controller()

@app.route("/api/create_or_replace_inventory_item", methods=['PUT'])
def create_or_replace_inventory_item():
    return ebay.create_or_replace_inventory_item_controller()

if __name__ == "__main__":
    app.run(debug=True)
