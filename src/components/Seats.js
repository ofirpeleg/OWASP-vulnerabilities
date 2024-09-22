import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Seats.css';

const Seats = ({ apiUrl, safeMode }) => {
    const [seats, setSeats] = useState({});
    const [user, setUser] = useState('');
    const [selectedSeats, setSelectedSeats] = useState([]);
    const navigate = useNavigate();

    const fetchSeats = useCallback(async () => {
        const response = await axios.get(`${apiUrl}/seats`);
        setSeats(response.data);
    }, [apiUrl]);

    useEffect(() => {
        fetchSeats();
    }, [fetchSeats]);

    const toggleSeatSelection = (seatNumber) => {
        if (selectedSeats.includes(seatNumber)) {
            setSelectedSeats(selectedSeats.filter((seat) => seat !== seatNumber));
        } else {
            setSelectedSeats([...selectedSeats, seatNumber]);
        }
    };

    const reserveSeats = async () => {
        try {
            const response = await axios.post(`${apiUrl}/reserve`, { user, seats: selectedSeats });
            if (response.data.status === "reserved") {
                navigate('/payment', { state: { seats: selectedSeats, user, safeMode } });
            } else {
                alert(response.data.reason);
            }
            fetchSeats();
        } catch (error) {
            alert('Reservation failed');
        }
    };

    return (
        <div className="container">
            <h1>Cinema Seat Reservation</h1>
            <div className="screen">Screen</div>
            <div className="seats">
                {Object.entries(seats).map(([seatNumber, reservedBy]) => (
                    <div 
                        key={seatNumber} 
                        className={`seat ${reservedBy ? 'reserved' : ''} ${selectedSeats.includes(seatNumber) ? 'selected' : ''}`}
                        onClick={() => !reservedBy && toggleSeatSelection(seatNumber)}
                    >
                        {seatNumber}
                    </div>
                ))}
            </div>
            <div className="form">
                <input 
                    type="text" 
                    placeholder="Your Name" 
                    value={user} 
                    onChange={(e) => setUser(e.target.value)} 
                />
                <button onClick={reserveSeats} disabled={selectedSeats.length === 0}>Reserve Seats</button>
            </div>
        </div>
    );
};

export default Seats;
