from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from search import search_flights

app = Flask(__name__)
CORS(app)
# load the flights.json file on startup to make it available for the search function
DATA_FILE = os.path.join(os.path.dirname(__file__), 'flights.json')

@app.route('/api/flights/search', methods=['GET'])
# get the origin, destination, and date from the request
def search():
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    date = request.args.get('date')

    if not origin or not destination or not date:
        return jsonify({"error": "Missing origin, destination, or date"}), 400
#Then we load the flights.json file
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 500

    results = search_flights(data, origin, destination, date)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
