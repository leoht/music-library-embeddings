import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchTracks } from '../api';
import SearchFilter from './SearchFilter';
import './components.css';

interface Track {
  _id: string;
  title: string;
}

const Tracks: React.FC = () => {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const loadTracks = async () => {
      try {
        const data = await fetchTracks();
        setTracks(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    };

    loadTracks();
  }, []);

  const filteredTracks = tracks.filter(track =>
    track.title.toLowerCase().includes(search.toLowerCase())
  );

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="container">
      <div className="tracks-container">
        <h2>Tracks</h2>
        <div className="search-filter">
          <SearchFilter value={search} onChange={setSearch} />
        </div>
        <ul className="tracks-list">
          {filteredTracks.map((track) => (
            <li key={track._id}>
              <Link to={`/tracks/${track._id}`}>{track.title}</Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Tracks; 