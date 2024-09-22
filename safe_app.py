from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading

app = Flask(__name__)
CORS(app)

# DB storage for seats and reservations
seats = {f"{row}{col}": None for row in range(2, 11) for col in range(1, 15)}
reservations = {}

lock = threading.Lock()

# Endpoint to reserve seats
@app.route('/reserve', methods=['POST'])
def reserve():
    global seats, reservations
    user = request.json['user']
    selected_seats = request.json['seats']
    
    with lock:
         # Check if all requested seats are available
        available = all(seat in seats and seats[seat] is None for seat in selected_seats)
        if available:
             # Set expiration time for the reservation (10 seconds)
            expiration_time = time.time() + 10  
            for seat in selected_seats:
                seats[seat] = user
            reservations[user] = {"seats": selected_seats, "expires": expiration_time}
            print(f"Reserved seats {selected_seats} for user {user} until {expiration_time}")
            return jsonify({"status": "reserved", "seats": selected_seats}), 200
        else:
            return jsonify({"status": "failed", "reason": "One or more seats already taken or does not exist"}), 400

@app.route('/release_expired', methods=['POST'])
# Endpoint to  trigger the release of expired reservations.
def release_expired():
    global seats, reservations
    current_time = time.time()
    with lock:
        # Identify users with expired reservations
        expired_users = [user for user, reservation in reservations.items() if reservation["expires"] < current_time]
        for user in expired_users:
            for seat in reservations[user]["seats"]:
                seats[seat] = None
            print(f"Releasing seats {reservations[user]['seats']} for expired user {user}")
            del reservations[user]
        return jsonify({"status": "expired reservations released"}), 200

@app.route('/seats', methods=['GET'])
# Endpoint to get the current status of all seats
def get_seats():
    return jsonify(seats), 200

def release_expired_reservations():
    # Background thread function to periodically release expired reservations.
    while True:
        time.sleep(10)  
        with app.app_context():
            current_time = time.time()
            with lock:
                expired_users = [user for user, reservation in reservations.items() if reservation["expires"] < current_time]
                for user in expired_users:
                    for seat in reservations[user]["seats"]:
                        seats[seat] = None
                    print(f"Background thread: Releasing seats {reservations[user]['seats']} for expired user {user}")
                    del reservations[user]
                if expired_users:
                    print(f"Background thread: Released expired reservations for users: {expired_users}")
                else:
                    print("Background thread: No expired reservations found")

if __name__ == '__main__':
    # Start the background thread to release expired reservations
    threading.Thread(target=release_expired_reservations, daemon=True).start()
    app.run(debug=True, port=5000)
