from flask import Flask, url_for
from flask import request as rq, render_template as rt, redirect as rd
import sqlite3 as sq
import random
import webbrowser
import threading

app = Flask(__name__)
def get_db_connection():
    conn = sq.connect('devices.db')
    conn.row_factory = sq.Row
    return conn

@app.route('/')
def index():
    return rd(url_for('register_device'))

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

@app.route('/signup_device', methods=['GET', 'POST'])
def register_device():
    if rq.method == 'POST':
        device_name = rq.form['device_name']
        ip_address = rq.form['ip_address']
        password = rq.form['password']

        # Input validation
        if not (device_name and ip_address and password):
            return rt('signup.html', message='All fields are required.')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO devices (device_name, ip_address, password) VALUES (?, ?, ?)",
                       (device_name, ip_address, password))
        conn.commit()
        conn.close()

        return rt('signup.html', message='Device added successfully!')
    
    return rt('signup.html')

@app.route('/signin_device', methods=['GET', 'POST'])
def check_availability():
    conn = get_db_connection()
    cursor = conn.cursor()

   
    cursor.execute("SELECT id, device_name FROM devices")
    devices = cursor.fetchall()

    if rq.method == 'POST':
        device_id = rq.form['device_id']
        password = rq.form['password']

        cursor.execute("SELECT password FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()

        if device is None:
            return rt('signin.html', devices=devices, message='Device not found.')

        if device['password'] != password:
            return rt('signin.html', devices=devices, message='Incorrect Password.')

        
        if random.randint(1, 100) % 2 == 0:
            return rt('signin.html', devices=devices, message='Reachable')
        else:
            return rt('signin.html', devices=devices, message='Not Reachable')
    
    return rt('signin.html', devices=devices)

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)