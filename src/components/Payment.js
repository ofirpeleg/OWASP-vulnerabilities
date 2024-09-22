import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Payment = ({ apiUrl }) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [timer, setTimer] = useState(10); 
    const seats = location.state.seats;
    const user = location.state.user;
    const safeMode = location.state.safeMode;

    useEffect(() => {
        if (safeMode) {
            const interval = setInterval(() => {
                setTimer((prevTimer) => prevTimer - 1);
            }, 1000);
            return () => clearInterval(interval);
        }
    }, [safeMode]);

    useEffect(() => {
        if (timer <= 0 && safeMode) {
            axios.post(`${apiUrl}/release_expired`, { user })
                .then(() => {
                    alert('Reservation expired! Returning to seat selection.');
                    navigate('/');
                });
        }
    }, [timer, safeMode, apiUrl, navigate, user]);

    const totalAmount = seats.length * 5;

    return (
        <div className="container">
            <h1>Payment</h1>
            <p>User: {user}</p>
            <p>Seats: {seats.join(', ')}</p>
            <p>Total Amount: ${totalAmount}</p>
            {safeMode && <p>Time remaining: {timer} seconds</p>}
        </div>
    );
};

export default Payment;
