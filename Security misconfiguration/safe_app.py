from flask import Flask, request, render_template_string, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'shenkar2024'

# MySQL database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='flask_app',
            user='root',
            password='admin1234'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT password FROM users WHERE username=%s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result and result[0] == password:
                    session['username'] = username
                    return 'Logged in successfully', 200
                else:
                    error = 'Invalid credentials'
                    status_code = 401  
            except Error:
                error = 'An error occurred. Please try again later.'
                status_code = 500  
            except Exception:
                error = 'An error occurred. Please try again later.'
                status_code = 500 
            finally:
                cursor.close()
                connection.close()
        else:
            error = 'Database connection failed'
            status_code = 500  
    
    return render_template_string(login_page_template, error=error), status_code

# Login page 
login_page_template = '''
<!doctype html>
<html>
<head>
    <title>Login</title>
</head>
<body>
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
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
