import React from 'react';

type SearchFilterProps = {
  value: string;
  onChange: (value: string) => void;
};

const SearchFilter: React.FC<SearchFilterProps> = ({ value, onChange }) => {
  return (
    <form style={{ marginBottom: '1rem' }} onSubmit={e => e.preventDefault()}>
      <input
        type="text"
        placeholder="Search tracks by name..."
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{ padding: '0.5rem', width: '100%', maxWidth: 300 }}
      />
    </form>
  );
};

export default SearchFilter; 