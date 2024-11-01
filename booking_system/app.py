from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="booking_system"
        )
    except Error as e:
        print(f"Error connecting to the database: {e}")
    return connection

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # Handle login logic
        return redirect(url_for('appointment'))
    return render_template('login.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        hall_type = request.form['hall_type']
        hall_number = request.form['hall_number']
        club_name = request.form['club_name']
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        event_type = request.form['event_type']
        name = request.form['name']
        dept = request.form['dept']
        email = request.form['email']

        db = get_db_connection()
        if db is not None:
            try:
                cursor = db.cursor(dictionary=True)
                cursor.execute("""
                    INSERT INTO bookings (hall_type, hall_number, club_name, event_name, event_date, event_time, event_type, name, dept, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (hall_type, hall_number, club_name, event_name, event_date, event_time, event_type, name, dept, email))
                db.commit()
            except Error as e:
                print(f"Error inserting into the database: {e}")
            finally:
                cursor.close()
                db.close()
        return redirect(url_for('status'))
    return render_template('appointment.html')

@app.route('/status')
def status():
    db = get_db_connection()
    bookings = []
    if db is not None:
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bookings")
            bookings = cursor.fetchall()
        except Error as e:
            print(f"Error fetching from the database: {e}")
        finally:
            cursor.close()
            db.close()
    return render_template('status.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
