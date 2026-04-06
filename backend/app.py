from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from search import search_flights

app = Flask(__name__)
CORS(app)
# load the flights.json file on startup to make it available for the search function
DATA_FILE = os.path.join(os.path.dirname(__file__), 'flights.json')
#Then we load the flights.json file
with open(DATA_FILE, 'r') as f:
    data = json.load(f)
#This is a list of all the airport codes
airport_codes = [airport['code'] for airport in data['airports']]

@app.route('/api/flights/search', methods=['GET'])
# get the origin, destination, and date from the request
def search():
    origin = request.args.get('origin', '').upper()
    destination = request.args.get('destination', '').upper()
    date = request.args.get('date')
    if not origin or not destination or not date:
        return jsonify({"error": "Missing origin, destination, or date"}), 400
    if origin not in airport_codes:
        return jsonify({"error": "Unknown origin airport code"}), 400
    if destination not in airport_codes:
        return jsonify({"error": "Unknown destination airport code"}), 400
    if origin == destination:
        return jsonify({"error": "Origin and destination must be different"}), 400
    results = search_flights(data, origin, destination, date)
    # return the results in a json format of origin, destination, date, count and itineraries
    return jsonify({
        "origin": origin,
        "destination": destination,
        "date": date,
        "count": len(results),
        "itineraries": results
    })
# health check endpoint
@app.route('/api/flights/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})
# get all airports
@app.route('/api/flights/airports', methods=['GET'])
def airports():
    return jsonify(data['airports'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
