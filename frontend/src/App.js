import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Testingsomething from './pages/Testingsomething';


const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Testingsomething />} />
            </Routes>
        </Router>
    );
};

export default App;
