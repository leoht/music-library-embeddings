import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Tracks from './src/components/Tracks';
import AddTrackForm from './src/components/AddTrackForm';
import TrackDetails from './src/components/TrackDetails';

const App = () => {
    return (
        <div className="app">
            {/* <h1>My music library</h1> */}
            <Router>
                <Routes>
                    <Route path="/" element={
                        <>
                            <Tracks />
                            <AddTrackForm />
                        </>
                    } />
                    <Route path="/tracks/:id" element={<TrackDetails />} />
                </Routes>
            </Router>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root')); 