from flask import Blueprint, request, jsonify
import sqlite3
import bcrypt

auth = Blueprint('auth', __name__)

# ─── SIGNUP ───────────────────────────────────────────────
@auth.route('/signup', methods=['POST'])
def signup():
    data      = request.get_json()
    full_name = data.get('full_name')
    email     = data.get('email')
    password  = data.get('password')
    confirm   = data.get('confirm_password')

    # Check passwords match
    if password != confirm:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn   = sqlite3.connect('alignai.db')
        cursor = conn.cursor()

        # INSERT query — saves user to database
        cursor.execute('''
            INSERT INTO users (full_name, email, password_hash)
            VALUES (?, ?, ?)
        ''', (full_name, email, password_hash))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Account created successfully'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 409


# ─── LOGIN ────────────────────────────────────────────────
@auth.route('/login', methods=['POST'])
def login():
    data     = request.get_json()
    email    = data.get('email')
    password = data.get('password')

    conn   = sqlite3.connect('alignai.db')
    cursor = conn.cursor()

    # SELECT query — finds user by email
    cursor.execute('''
        SELECT id, full_name, password_hash
        FROM users
        WHERE email = ?
    ''', (email,))

    user = cursor.fetchone()
    conn.close()

    # Check user exists and password is correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        return jsonify({
            'message'  : 'Login successful',
            'user_id'  : user[0],
            'full_name': user[1]
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401