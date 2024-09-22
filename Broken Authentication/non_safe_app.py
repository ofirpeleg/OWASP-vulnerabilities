from flask import Flask, request, render_template_string, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'shenkar2024'

# DB storage for demonstration purpose
users = {
    'ofirpeleg2111@gmail.com': generate_password_hash('1234'),
    'user2': generate_password_hash('mypassword')
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_password_hash = users.get(username)
        if user_password_hash and check_password_hash(user_password_hash, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            status_code = 401  
    return render_template_string(login_page_template, error=error), status_code

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
  <label for="username">Username:</label><br>
  <input type="text" id="username" name="username"><br>
  <label for="password">Password:</label><br>
  <input type="password" id="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
{% if error %}
<p style="color: red;">{{ error }}</p>
{% endif %}
'''

if __name__ == '__main__':
    app.run(debug=True)
