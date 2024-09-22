import logging
import time
import random
from flask import Flask, request, render_template_string, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import pyotp
import smtplib
from email.mime.text import MIMEText


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'shenkar2024'

# Email configuration for Gmail

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = '*****'  
SMTP_PASSWORD = '******'         
FROM_EMAIL = '******'     

# DB storage for demonstration purpose
users = {
    'ofirpeleg2111@gmail.com': generate_password_hash('1234'),
    'user2@example.com': generate_password_hash('mypassword')
}

# MFA secret storage for demonstration purposes

mfa_secrets = {
    'ofirpeleg2111@gmail.com': pyotp.random_base32(),
    'user2@example.com': pyotp.random_base32()
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            # checks if the given email is valid
            validate_email(username)
            user_password_hash = users.get(username)
            if user_password_hash and check_password_hash(user_password_hash, password):
                session['username'] = username
                session['mfa_required'] = True
                send_otp_email(username)
                return redirect(url_for('mfa'))
            else:
                error = 'Invalid credentials. Please try again.'
                status_code = 401 
        except EmailNotValidError as e:
            error = str(e)
            status_code = 400  
    return render_template_string(login_page_template, error=error), status_code

# function that sends an OTP to the user's email
def send_otp_email(to_email):
    otp = random.randint(100000, 999999)
    session['otp'] = otp
    session['otp_expiration'] = time.time() + 300  # valid for 5 minutes
    subject = 'Your MFA OTP'
    body = f'Your OTP is: {otp}'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    # Log the OTP sent by the server
    logging.debug(f'Sending OTP {otp} to {to_email}')

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())

@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if 'mfa_required' not in session:
        return redirect(url_for('login'))
    error = None
    status_code = 200  
    if request.method == 'POST':
        otp = request.form['token']
        username = session['username']
        stored_otp = session.get('otp')
        otp_expiration = session.get('otp_expiration')

        logging.debug(f'User {username} entered OTP {otp}')

        # Verify the OTP
        if stored_otp and otp_expiration and time.time() < otp_expiration:
            if int(otp) == stored_otp:
                session.pop('mfa_required', None)
                session.pop('otp', None)
                session.pop('otp_expiration', None)
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid OTP. Please try again.'
                status_code = 401  
        else:
            error = 'OTP expired. Try again.'
            status_code = 401  
    return render_template_string(mfa_page_template, error=error), status_code

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Welcome {session["username"]} to your dashboard!'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Login page 
login_page_template = '''
<!doctype html>
<title>Login</title>
<h1>Login</h1>
<form method="post">
  <label for="username">Email:</label><br>
  <input type="text" id="username" name="username"><br>
  <label for="password">Password:</label><br>
  <input type="password" id="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
{% if error %}
<p style="color: red;">{{ error }}</p>
{% endif %}
'''

# MFA page 
mfa_page_template = '''
<!doctype html>
<title>MFA</title>
<h1>Multi-Factor Authentication</h1>
<form method="post">
  <label for="token">OTP:</label><br>
  <input type="text" id="token" name="token"><br><br>
  <input type="submit" value="Verify">
</form>
{% if error %}
<p style="color: red;">{{ error }}</p>
{% endif %}
'''

if __name__ == '__main__':
    app.run(debug=True)
