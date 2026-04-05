import datetime
import pytz

def search_flights(data, origin, destination, date_str):
    """
    Search for flights between origin and destination on a given date.
    """
    # Parse the date
    search_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Get all flights
    flights = data['flights']
    
    # Filter flights by date
    flights = [f for f in flights if datetime.datetime.strptime(f['departureTime'], '%Y-%m-%dT%H:%M:%S').date() == search_date]
    
    # Filter flights by origin and destination
    flights = [f for f in flights if f['origin'] == origin and f['destination'] == destination]
    
    return flights
