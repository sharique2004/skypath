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
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        return jsonify(error='Invalid date format. Expected YYYY-MM-DD'), 400
    if date < datetime.date.today():
        return jsonify(error='Date cannot be in the past'), 400
    if date > datetime.date.today() + datetime.timedelta(days=365):
        return jsonify(error='Date cannot be more than 365 days in the future'), 400
    if date == datetime.date.today():
        return jsonify(error='Date cannot be today'), 400

    results = search_flights(data, origin, destination, date)
    return jsonify(results)
@app.route('/api/flights/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/flights/airports', methods=['GET'])
def airports():
    if not origin or not destination or not date:
        return jsonify({"error": "Missing origin, destination, or date"}), 400
    if origin not in airport_codes:
        return jsonify({"error": "Unknown origin airport code"}), 400
    if destination not in airport_codes:
        return jsonify({"error": "Unknown destination airport code"}), 400
    if origin == destination:
        return jsonify({"error": "Origin and destination must be different"}), 400
    return jsonify(data['airports'])

@app.route('/api/flights/flights', methods=['GET'])
def flights():
    return jsonify(data['flights'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
