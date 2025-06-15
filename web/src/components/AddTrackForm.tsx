import React, { useState, FormEvent, ChangeEvent } from 'react';
import { addTrack } from '../api';
import './components.css';

const AddTrackForm: React.FC = () => {
  const [trackName, setTrackName] = useState('');
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!audioFile) {
      setError('Please select an audio file');
      return;
    }

    try {
      await addTrack(trackName, audioFile);
      setTrackName('');
      setAudioFile(null);
      setSuccess(true);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setSuccess(false);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAudioFile(e.target.files[0]);
    }
  };

  return (
    <div className="container">
      <form className="add-track-form" onSubmit={handleSubmit}>
        <h3>Upload a new track</h3>
        <div>
          <input
            type="text"
            placeholder="Track name"
            value={trackName}
            onChange={(e) => setTrackName(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            required
          />
        </div>
        <button type="submit">Upload Track</button>
        {error && <div style={{ color: 'red', marginTop: '1rem' }}>{error}</div>}
        {success && <div style={{ color: 'green', marginTop: '1rem' }}>Track uploaded successfully!</div>}
      </form>
    </div>
  );
};

export default AddTrackForm; 