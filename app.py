import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_mysqldb import MySQL
from datetime import datetime, date
import mysql.connector
from flask import render_template
import bcrypt
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'ff80b591e8778b991e81613ad5b641182fddbe7769eb1dba'

# Database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nandy'
app.config['MYSQL_DB'] = 'hospital_inventory'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')  
    password = request.form.get('password')
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, password, role FROM Users WHERE name = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        session['user_id'] = user[0]
        session['role'] = user[2]
        
        if user[2] == 'member':
            return redirect(url_for('equipment_search'))
        elif user[2] == 'manager':
            return redirect(url_for('view_orders'))
        
    return "Invalid credentials", 401

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        role = request.form['role']

        if role not in ['member', 'manager']:
            return "Invalid role", 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user1 (name, password, role) VALUES (%s, %s, %s)", (name, hashed_password, role))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('signup.html')

@app.route('/equipment_search', methods=['GET', 'POST'])
def equipment_search():
    if request.method == 'POST':
        name = request.form['search_name']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Equipment WHERE name LIKE %s AND quantity > threshold", (f"%{name}%",))
        equipment = cursor.fetchall()
        cursor.close()
        if not equipment:
            return "NO Stock"

        return render_template('equipment_search.html', equipment=equipment)

    return render_template('equipment_search.html')

@app.route('/request_usage', methods=['POST'])
def request_usage():
    equipment_id = request.form['equipment_id']
    room_requested = request.form['room_requested']
    requested_by = session['user_id']  # Assuming this will be the user_id of the member

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT quantity, threshold FROM Equipment WHERE equipment_id = %s", (equipment_id,))
    equipment = cursor.fetchone()
    
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404

    quantity, threshold = equipment
    if quantity <= threshold:
        cursor.execute("""
            INSERT INTO Orders (equipment_id, order_type, quantity_ordered, order_date, requested_by, room_requested, status)
            VALUES (%s, 'New Order', %s, NOW(), %s, %s, 'Pending')
        """, (equipment_id, threshold - quantity + 1, requested_by, room_requested))
    else:
        cursor.execute("""
            INSERT INTO Orders (equipment_id, order_type, quantity_ordered, order_date, requested_by, room_requested, status)
            VALUES (%s, 'Usage Request', 1, NOW(), %s, %s, 'Pending')
        """, (equipment_id, requested_by, room_requested))

    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('equipment_search'))

@app.route('/view_orders')
def view_orders():
    if session.get('role') != 'manager':
        return "Access denied", 403
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    cursor.execute("""
        SELECT o.order_id, o.equipment_id, e.name AS equipment_name, o.quantity_ordered, o.order_date, o.room_requested, o.approval_status
        FROM Orders o
        JOIN Equipment e ON o.equipment_id = e.equipment_id
        WHERE o.approval_status = 'Pending'
    """)
    orders = cursor.fetchall()
    cursor.close()
    return render_template('view_orders.html', orders=orders)

@app.route('/approve_order/<int:order_id>', methods=['POST'])
def approve_order(order_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Retrieve the order to get the equipment ID and quantity ordered
    cursor.execute("SELECT equipment_id, quantity_ordered FROM Orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()
    
    if order:
        equipment_id = order['equipment_id']
        quantity_ordered = order['quantity_ordered']
        
        # Update the order's approval status
        cursor.execute("UPDATE Orders SET approval_status = 'Approved' WHERE order_id = %s", (order_id,))
        
        # Deduct the quantity from the Equipment table
        cursor.execute("UPDATE Equipment SET quantity = quantity - %s WHERE equipment_id = %s", (quantity_ordered, equipment_id))
        
        mysql.connection.commit()
        cursor.close()
        
        # Return success response
        return jsonify({"success": True})
    
    cursor.close()
    return jsonify({"success": False}), 400

@app.route('/reject_order/<int:order_id>', methods=['POST'])
def reject_order(order_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Orders SET approval_status = 'Rejected' WHERE order_id = %s", (order_id,))
    mysql.connection.commit()
    cursor.close()

    # Respond with success message
    return jsonify({'success': True})

@app.route('/manager/orders')
def view_all_orders():
    cursor = mysql.connection.cursor()
    query = '''SELECT o.order_id, e.name AS equipment_name, o.quantity_ordered, o.order_date, o.room_requested, o.approval_status
        FROM Orders o
        JOIN Equipment e ON o.equipment_id = e.equipment_id'''
    cursor.execute(query)
    orders = cursor.fetchall()
    cursor.close()
    return render_template('all_orders.html', orders=orders)

# Route to display orders that require placement with recommended dealers
@app.route('/manager/orders_to_place')
def view_orders_to_place():
    cursor = mysql.connection.cursor()
    query = '''SELECT 
            o.order_id, o.order_date, d.name, d.contact_info, d.address, e.name
            FROM Orders o
            LEFT JOIN Dealers d ON o.equipment_id = d.dealer_id
            LEFT JOIN Equipment e ON o.equipment_id = e.equipment_id
            WHERE o.approval_status = 'Pending' && e.threshold > e.quantity'''
    cursor.execute(query)
    orders_to_place = cursor.fetchall()
    print(orders_to_place)
    cursor.close()
    return render_template('orders_to_place.html', orders=orders_to_place)


if __name__ == "__main__":
    app.run(debug=True)