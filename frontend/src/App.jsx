import { useState } from 'react'
import SearchForm from './components/SearchForm'
import './App.css'

function App() {
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = (origin, destination, date) => {
    console.log("We will send this to the backend shortly:", origin, destination, date);
    setIsLoading(true);

    // Just faking a loading state for 1 second right now to test our button
    setTimeout(() => setIsLoading(false), 1000);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>SkyPath Search</h1>
        <p>Where your journey begins.</p>
      </header>

      <main>
        <SearchForm onSearch={handleSearch} isLoading={isLoading} />
      </main>
    </div>
  )
}

export default App
