from flask import Flask, request, render_template_string, session
import mysql.connector
from mysql.connector import Error
import re

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
# for logging purposes only - if the table exist or not
def log_table_names(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            table_names = [table[0] for table in tables]
            print(f"Tables in the database: {table_names}")
        else:
            print("Tables in the database: none")
    except Error as e:
        print(f"Error retrieving table names: {e}")

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            try:
                log_table_names(connection)  
                cursor = connection.cursor()
                query = f"SELECT password FROM users WHERE username='{username}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if result and result[0] == password:
                    session['username'] = username
                    return 'Logged in successfully', 200
                else:
                    error = 'Invalid credentials'
                    return render_template_string(login_page_template, error=error), 401
            except mysql.connector.errors.ProgrammingError as e:
                if "1146" in str(e):  # table doesn't exist code
                    print("Table 'users' does not exist")
                import traceback
                stack_trace = traceback.format_exc()
                error = f"SQL Error: {str(e)}\n\n{stack_trace}"
                return render_template_string(login_page_template, error=error), 500
            except Error as e:
                import traceback
                stack_trace = traceback.format_exc()
                error = f"SQL Error: {str(e)}\n\n{stack_trace}"
                return render_template_string(login_page_template, error=error), 500
            except Exception as e:
                import traceback
                stack_trace = traceback.format_exc()
                error = f"General Error: {str(e)}\n\n{stack_trace}"
                return render_template_string(login_page_template, error=error), 500
            finally:
                cursor.close()
                connection.close()
        else:
            error = 'Database connection failed'
            return render_template_string(login_page_template, error=error), 500

    return render_template_string(login_page_template, error=error)

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
    <p style="color: red; white-space: pre-wrap;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
