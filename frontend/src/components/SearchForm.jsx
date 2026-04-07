import { useState } from 'react';

export default function SearchForm({ onSearch, isLoading }) {
    const [origin, setOrigin] = useState('');
    const [destination, setDestination] = useState('');
    const [date, setDate] = useState('2024-03-15'); // using this default per instructions

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(origin, destination, date);
    };

    return (
        <div className="search-card">
            <form onSubmit={handleSubmit} className="search-form">
                <div className="input-group">
                    <label>Origin</label>
                    <input
                        type="text"
                        placeholder="e.g. JFK"
                        maxLength="3"
                        value={origin}
                        onChange={(e) => setOrigin(e.target.value.toUpperCase())}
                        required
                    />
                </div>

                <div className="input-group">
                    <label>Destination</label>
                    <input
                        type="text"
                        placeholder="e.g. LAX"
                        maxLength="3"
                        value={destination}
                        onChange={(e) => setDestination(e.target.value.toUpperCase())}
                        required
                    />
                </div>

                <div className="input-group">
                    <label>Date</label>
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                </div>

                <button type="submit" className="search-button" disabled={isLoading}>
                    {isLoading ? 'Searching...' : 'Find Flights'}
                </button>
            </form>
        </div>
    );
}
