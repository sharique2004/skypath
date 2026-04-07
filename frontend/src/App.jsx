import { useState } from 'react';
import SearchForm from './components/SearchForm';
import FlightResults from './components/FlightResults';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [itineraries, setItineraries] = useState(null);

  const handleSearch = async (origin, destination, date) => {
    setIsLoading(true);
    setError(null);
    setItineraries(null);

    try {
      // 1. We talk to the Python backend you have running on port 5000!
      const response = await fetch(`/api/flights/search?origin=${origin}&destination=${destination}&date=${date}`);


      const data = await response.json();

      // 2. We check if the backend gave us an error (like an invalid airport code)
      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong fetching flights.');
      }

      // 3. We save the results into our React state, which automatically updates the screen!
      setItineraries(data.itineraries);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>SkyPath Search</h1>
        <p>Find the best multi-stop flight connections.</p>
      </header>

      <main>
        <SearchForm onSearch={handleSearch} isLoading={isLoading} />

        {/* If we have an error, show it in a nice red box */}
        {error && (
          <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', padding: '1rem', borderRadius: '8px', marginBottom: '2rem', textAlign: 'center', border: '1px dashed #ef4444' }}>
            Error: {error}
          </div>
        )}

        {/* If we successfully searched, show the results! */}
        {itineraries && <FlightResults itineraries={itineraries} />}
      </main>
    </div>
  )
}

export default App;
