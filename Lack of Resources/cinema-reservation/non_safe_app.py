from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# DB storage for seats
seats = {f"{row}{col}": None for row in range(2, 11) for col in range(1, 15)}

lock = threading.Lock()

@app.route('/reserve', methods=['POST'])
def reserve():
    global seats
    user = request.json['user']
    selected_seats = request.json['seats']
    
    with lock:
        available = all(seat in seats and seats[seat] is None for seat in selected_seats)
        if available:
            for seat in selected_seats:
                seats[seat] = user
            return jsonify({"status": "reserved", "seats": selected_seats}), 200
        else:
            return jsonify({"status": "failed", "reason": "One or more seats already taken or does not exist"}), 400

@app.route('/seats', methods=['GET'])
def get_seats():
    return jsonify(seats), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
