import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchTrack } from '../api';
import './components.css';

interface Track {
  _id: string;
  title: string;
  timestamp: string;
}

interface SimilarTrack {
  _id: string;
  title: string;
  timestamp: string;
}

interface TrackResponse extends Track {
  similar_tracks: SimilarTrack[];
}

const TrackDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [track, setTrack] = useState<TrackResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTrack = async () => {
      if (!id) return;
      try {
        const data = await fetchTrack(id);
        setTrack(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    };

    loadTrack();
  }, [id]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!track) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container">
      <div className="track-details">
        <Link to="/" className="back-link">Back to library</Link>
        <h3>{track.title}</h3>
        <p>Created: {new Date(track.timestamp).toLocaleString()}</p>
        
        <div>
          <h4>Similar Tracks</h4>
          {track.similar_tracks.length > 0 ? (
            <ul className="similar-tracks-list">
              {track.similar_tracks.map((similarTrack) => (
                <li key={similarTrack._id}>
                  <Link to={`/tracks/${similarTrack._id}`}>{similarTrack.title}</Link>
                </li>
              ))}
            </ul>
          ) : (
            <p>No similar tracks found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TrackDetails; 