import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Seats from './components/Seats';
import Payment from './components/Payment';

function App() {
    const apiUrl = "http://127.0.0.1:5000"; 
    const safeMode = true; // indicates safe or Unsafe application (timer)

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Seats apiUrl={apiUrl} safeMode={safeMode} />} />
                <Route path="/payment" element={<Payment apiUrl={apiUrl} />} />
            </Routes>
        </Router>
    );
}

export default App;