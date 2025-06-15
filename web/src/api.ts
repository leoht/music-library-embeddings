export const fetchTracks = async () => {
  const response = await fetch('http://localhost:8000/tracks');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const addTrack = async (title: string, file: File) => {
  const formData = new FormData();
  formData.append('track_name', title);
  formData.append('audio_file', file);

  const response = await fetch('http://localhost:8000/tracks', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
};

export const fetchTrack = async (id: string) => {
    const response = await fetch(`http://localhost:8000/tracks/${id}`);
    if (!response.ok) {
        throw new Error('Failed to fetch track');
    }
    return response.json();
}; 