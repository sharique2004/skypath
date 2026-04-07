export default function FlightResults({ itineraries }) {
    if (!itineraries || itineraries.length === 0) {
        return (
            <div className="empty-state">
                <p>No flights found for this route. Try another search.</p>
            </div>
        );
    }

    return (
        <div className="results-container">
            <h3>{itineraries.length} Flight Options Built For You</h3>

            <div className="itinerary-list">
                {itineraries.map((itinerary, index) => (
                    <div key={index} className="itinerary-card">
                        <div className="itinerary-header">
                            <div className="duration">
                                <strong>{itinerary.totalDuration}</strong> total travel time
                            </div>
                            <div className="price">
                                ${itinerary.totalPrice.toFixed(2)}
                            </div>
                        </div>

                        <div className="segments-list">
                            {itinerary.segments.map((segment, sIdx) => {
                                // Calculate if there's a layover after this segment
                                const layover = itinerary.layovers && itinerary.layovers[sIdx];

                                return (
                                    <div key={sIdx}>
                                        <div className="segment">
                                            <div className="segment-airline">
                                                {segment.airline} • {segment.flightNumber}
                                            </div>
                                            <div className="segment-route">
                                                <div className="route-point">
                                                    <div className="time">{new Date(segment.departureTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                                                    <div className="airport">{segment.originCity} ({segment.origin})</div>
                                                </div>
                                                <div className="route-line"></div>
                                                <div className="route-point">
                                                    <div className="time">{new Date(segment.arrivalTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                                                    <div className="airport">{segment.destinationCity} ({segment.destination})</div>
                                                </div>
                                            </div>
                                        </div>

                                        {layover && (
                                            <div className="layover-box">
                                                <span>{layover.duration} layover in {layover.city} ({layover.airport})</span>
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
