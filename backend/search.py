from datetime import datetime
from collections import defaultdict
import pytz

# convert local airport time to UTC so we can compare times across timezones
def to_utc(time_str, tz_name):
    tz = pytz.timezone(tz_name)
    dt = datetime.fromisoformat(time_str)
    return tz.localize(dt).astimezone(pytz.utc)

# figure out how many minutes between one flight landing and the next one taking off
def get_layover(flight1, flight2, airports):
    arr_tz = airports[flight1['destination']]['timezone']
    dep_tz = airports[flight2['origin']]['timezone']
    arr_time = to_utc(flight1['arrivalTime'], arr_tz)
    dep_time = to_utc(flight2['departureTime'], dep_tz)
    return (dep_time - arr_time).total_seconds() / 60

# check if all airports in the connection are in the same country
def is_domestic(flight1, flight2, airports):
    countries = {
        airports[flight1['origin']]['country'],
        airports[flight1['destination']]['country'],
        airports[flight2['destination']]['country'],
    }
    return len(countries) == 1

# check if the connection between two flights is valid based on the rules
def valid_connection(flight1, flight2, airports):
    # passengers cant change airports during layover
    if flight1['destination'] != flight2['origin']:
        return False
    
    mins = get_layover(flight1, flight2, airports)
    
    # next flight has to leave after the first one lands
    if mins <= 0:
        return False
    # max 6 hour layover
    if mins > 360:
        return False
    # domestic = 45 min, international = 90 min minimum
    min_wait = 45 if is_domestic(flight1, flight2, airports) else 90
    return mins >= min_wait

# just formats minutes into something readable
def fmt_duration(mins):
    return f"{int(mins // 60)}h {int(round(mins % 60))}m"

# takes list of flights and builds a nice response with all the details
def make_itinerary(flights, airports):
    # calculate layover info at each stop
    layovers = []
    for i in range(len(flights) - 1):
        mins = get_layover(flights[i], flights[i+1], airports)
        stop = flights[i]['destination']
        layovers.append({
            "airport": stop,
            "airportName": airports[stop]['name'],
            "city": airports[stop]['city'],
            "duration": fmt_duration(mins),
            "durationMinutes": mins
        })
    
    # total travel time from start to finish
    first = flights[0]
    last = flights[-1]
    start = to_utc(first['departureTime'], airports[first['origin']]['timezone'])
    end = to_utc(last['arrivalTime'], airports[last['destination']]['timezone'])
    total_mins = (end - start).total_seconds() / 60
    
    total_price = sum(float(f['price']) for f in flights)
    
    return {
        "segments": [{
            "flightNumber": f['flightNumber'],
            "airline": f['airline'],
            "origin": f['origin'],
            "originCity": airports[f['origin']]['city'],
            "destination": f['destination'],
            "destinationCity": airports[f['destination']]['city'],
            "departureTime": f['departureTime'],
            "arrivalTime": f['arrivalTime'],
            "aircraft": f['aircraft'],
            "price": float(f['price'])
        } for f in flights],
        "layovers": layovers,
        "totalDuration": fmt_duration(total_mins),
        "totalDurationMinutes": total_mins,
        "totalPrice": round(total_price, 2),
        "stops": len(flights) - 1
    }


def search_flights(data, origin, destination, date_str):
    # build lookup dicts so we dont have to loop through arrays every time
    airports = {a['code']: a for a in data['airports']}
    
    # group all flights by where they depart from (only flights on the search date)
    by_origin = defaultdict(list)
    for f in data['flights']:
        if f['departureTime'].startswith(date_str):
            by_origin[f['origin']].append(f)
    
    results = []
    
    # go through every flight leaving from our starting airport
    for leg1 in by_origin.get(origin, []):
        
        # direct flight - goes straight to where we want
        if leg1['destination'] == destination:
            results.append(make_itinerary([leg1], airports))
            continue
        
        # not direct, so check flights from where leg1 lands
        stop1 = leg1['destination']
        for leg2 in by_origin.get(stop1, []):
            if not valid_connection(leg1, leg2, airports):
                continue
            
            # 1 stop connection
            if leg2['destination'] == destination:
                results.append(make_itinerary([leg1, leg2], airports))
                continue
            
            # try one more hop for 2 stop connections
            stop2 = leg2['destination']
            if stop2 == origin or stop2 == stop1:
                continue
            
            for leg3 in by_origin.get(stop2, []):
                if leg3['destination'] != destination:
                    continue
                if not valid_connection(leg2, leg3, airports):
                    continue
                results.append(make_itinerary([leg1, leg2, leg3], airports))
    
    # shortest trips first
    def by_duration(itinerary):
        return itinerary['totalDurationMinutes']
    results.sort(key=by_duration)
    return results