from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import re
import random
import hashlib
import os

def validate_input(input_data):
    '''
    Validates user input for XSS and SQL injection prevention.
    :param input_data: The user input to validate.
    :return: (bool, str) - A tuple where the first value is True if valid, False otherwise, and the second value is the sanitized input.
    '''
    if not isinstance(input_data, str):
        return False, None

    # Check for malicious patterns
    forbidden_patterns = [
        r"(--|\bOR\b|\bAND\b|;|#|')",  # Prevent SQL injection patterns
        r"(<script>|<\/script>|<img|onerror|onload)",  # Prevent XSS
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, input_data, re.IGNORECASE):
            return False, None

    # Sanitize input
    sanitized_input = re.sub(r"[^\w\s@.-]", "", input_data)  # Allow alphanumeric, spaces, @, ., and -
    return True, sanitized_input
app = Flask(__name__)
app.secret_key = 'secret key'

conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    port = 8889,
    db = 'donationDB',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

def salt_and_hash(salt, password):
    if salt == -1:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt)  # Convert hexadecimal to bytes
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    return salt.hex(), hashed_password

@app.route('/test')
def health():
    return 'connected!'

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    cursor.execute('SELECT password, salt FROM person WHERE username = %s', (username, ))
    data = cursor.fetchone()
    cursor.close()

    if (data):
        salt = data['salt']
        hashed_password = data['password']

        _, check_hash = salt_and_hash(salt, password)
        if check_hash == hashed_password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)
    else:
        error = 'Invalid login'
        return render_template('login.html', error=error)
    
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# TODO: add register
@app.route('/registerUser', methods=['POST'])
def registerUser():
    username = request.form.get('username')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    role = request.form.get('role')

    if not (username and password and fname and lname and email and role):
        flash("Please fill out all fields.")
        return redirect(url_for('register'))
    
    salt, hashed_password = salt_and_hash(-1, password)

    cursor = conn.cursor()

    cursor.execute("SELECT userName FROM Person WHERE userName=%s", (username,))
    user_exists = cursor.fetchone()

    if user_exists:
        flash("Username already taken, please choose another.")
        return redirect(url_for('register'))

    cursor.execute('''
        INSERT INTO Person (userName, password, salt, fname, lname, email)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (username, hashed_password, salt, fname, lname, email))

    cursor.execute('''
        INSERT INTO act VALUES (%s, %s)
    ''', (username, role))

    cursor.close()
    flash("Registration successful! Please log in.")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login')) 
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

# TODO: Find single item [ELI]
# route to find item webpage
@app.route('/find_single_item_page')
def find_single_item_page():
    return render_template('find_single_item.html')

@app.route('/find_single_item', methods=['GET', 'POST'])
def find_single_item():
    pieces = []
    if request.method == 'POST':
        item_id = request.form['item_id']

        # Check if item_id is valid
        is_valid, sanitized_item_id = validate_input(item_id)
        if not is_valid:
            flash('Invalid query. Please try again.')
            return render_template('find_single_item.html', pieces=[])

        cursor = conn.cursor()
        query = ('SELECT pieceNum, pDescription, roomNum, shelfNum, pNotes '
                 'FROM Piece '
                 'WHERE itemID = %s')
        cursor.execute(query, (sanitized_item_id,))
        pieces = cursor.fetchall()
        cursor.close()
    return render_template('find_single_item.html', pieces=pieces)

# TODO: Find order items [ELI]
@app.route('/find_order_items_page')
def find_order_items_page():
    return render_template('find_order_items.html')

@app.route('/find_order_items', methods=['GET', 'POST'])
def find_order_items():
    items =[]
    if request.method == 'POST':
        order_id = request.form['order_id']

        # Check if item_id is valid
        is_valid, sanitized_order_id = validate_input(order_id)
        if not is_valid:
            flash('Invalid query. Please try again.')
            return render_template('find_order_items.html', items=[])

        cursor = conn.cursor()
        query = ('SELECT ItemIn.itemID, Piece.pieceNum, Piece.pDescription, '
                 'Piece.roomNum, Piece.shelfNum, Piece.pNotes '
                 'FROM ItemIn '
                 'JOIN Piece ON ItemIn.itemID = Piece.itemID '
                 'WHERE ItemIn.orderID = %s')
        cursor.execute(query, (sanitized_order_id,))
        items = cursor.fetchall()
        cursor.close()
    return render_template('find_order_items.html', items=items)

# TODO: Accept donation [ELI]
@app.route('/accept_donation_page')
def accept_donation_page():
    return render_template('accept_donation.html')

@app.route('/accept_donation', methods=['GET', 'POST'])
def accept_donation():
    if request.method == 'POST':
        # Retrieve form data
        staff_username = request.form['staff_username']
        donor_username = request.form['donor_username']
        item_description = request.form['item_description']
        item_photo = request.form.get('item_photo')
        item_color = request.form.get('item_color')
        item_material = request.form['item_material']
        main_category = request.form['item_category']
        sub_category = request.form['item_subcategory']
        pieces = list(zip(
            request.form.getlist('piece_description'),
            request.form.getlist('piece_length'),
            request.form.getlist('piece_width'),
            request.form.getlist('piece_height'),
            request.form.getlist('piece_room'),
            request.form.getlist('piece_shelf'),
            request.form.getlist('piece_notes')
        ))

        # Validate staff member
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Act WHERE userName = %s AND roleID = %s', (staff_username, 'Staff'))
        staff = cursor.fetchone()
        if not staff:
            flash('Invalid staff username.')
            return render_template('accept_donation.html')

        # Validate donor
        cursor.execute('SELECT * FROM Act WHERE userName = %s AND roleID = %s', (donor_username, 'Donor'))
        donor = cursor.fetchone()
        if not donor:
            flash('Invalid donor username.')
            return render_template('accept_donation.html')

        # Insert Item
        cursor.execute(
            'INSERT INTO Item (iDescription, photo, color, material, hasPieces, mainCategory, subCategory) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (item_description, item_photo, item_color, item_material, True, main_category, sub_category)
        )
        item_id = cursor.lastrowid
        print(f"Inserted ItemID: {item_id}")

        # Insert DonatedBy
        cursor.execute(
            'INSERT INTO DonatedBy (ItemID, userName, donateDate) VALUES (%s, %s, CURDATE())',
            (item_id, donor_username)
        )

        # Insert Pieces
        piece_num = 1
        for desc, length, width, height, room, shelf, notes in pieces:
            # Skip blank entries for pieces to avoid bad data
            if not desc.strip():
                continue
            cursor.execute(
                'INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (item_id, piece_num, desc, length, width, height, room, shelf, notes)
            )
            piece_num += 1

        conn.commit()
        cursor.close()

        # Store a success flag in the session for scoping flash messages
        session['donation_success'] = True
        return redirect(url_for('accept_donation'))

    # Check for donation success
    donation_success = session.pop('donation_success', None)
    if donation_success:
        flash('Donation successfully recorded!')
        return redirect(url_for('accept_donation'))

    return render_template('accept_donation.html')

# TODO: Start an order [IAN]

@app.route('/start_order_page')
def start_order_page():
    return render_template('start_order.html')

@app.route('/start_order', methods=['GET', 'POST'])
def start_order():
    if request.method == 'POST':
        # Retrieve form data
        staff_username = request.form['staff_username']
        client_username = request.form['client_username']

        # Validate staff member
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Act WHERE userName = %s AND roleID = %s', (staff_username, '2'))
        staff = cursor.fetchone()
        if not staff:
            flash('Invalid staff username.')
            return render_template('start_order.html')

        # Validate client
        cursor.execute('SELECT * FROM Act WHERE userName = %s AND roleID = %s', (client_username, '1'))
        client = cursor.fetchone()
        if not client:
            flash('Invalid client username.')
            return render_template('start_order.html')


        cursor.execute("SELECT orderID FROM Ordered")
        #existing_ids = {row[0] for row in cursor.fetchall()}
        
        orders = cursor.fetchone()
        
        # Generate a unique 5-digit number
        while True:
            new_id = random.randint(10000, 99999)  
            if new_id not in orders:
                break
        
        session['start_order_numer'] = new_id

        #item_id = cursor.lastrowid
        print(f"Your orderID is: {session.get('start_order_numer')}")
        
        
        conn.commit()
        cursor.close()

        return redirect(url_for('start_order'))

    return render_template('start_order.html')



# TODO: Add to current order [IAN]

# TODO: Prepare order [IAN]

# TODO: User's tasks [CHETAN]
@app.route('/userTasks_page', methods = ['GET'])
def userTasks_page():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_page'))
    return render_template('usertasks.html')

@app.route('/get_user_tasks', methods = ['GET'])
def get_user_tasks():
    cursor = conn.cursor()
    username = session.get('username')

    cursor.execute('''
        SELECT orderID, orderDate, orderNotes, supervisor, client
        FROM Ordered
        WHERE client = %s
        ''', (username,))
    client = cursor.fetchall()

    cursor.execute('''
        SELECT o.orderID, o.orderDate, o.orderNotes, o.supervisor, o.client
        FROM Ordered o
        WHERE o.supervisor = %s
        ''', (username,))
    supervisor = cursor.fetchall()

    cursor.execute('''
        SELECT a.userName, a.roleID, r.rDescription
        FROM Act a
        JOIN Role r ON a.roleID = r.roleID
        WHERE a.userName = %s
        ''', (username,))
    volunteer = cursor.fetchall()

    cursor.execute('''
        SELECT d.ItemID, d.donateDate, i.iDescription
        FROM DonatedBy d
        JOIN Item i ON d.ItemID = i.ItemID
        WHERE d.userName = %s
        ''', (username,))
    donated = cursor.fetchall()

    cursor.execute('''
        SELECT o.orderID, o.orderDate, d.status, d.date
        FROM Delivered d
        JOIN Ordered o ON d.orderID = o.orderID
        WHERE d.userName = %s
        ''', (username,))
    delivered = cursor.fetchall()
    
    cursor.close()

    return render_template('usertasks.html', client=client, supervisor=supervisor, volunteer=volunteer, donated=donated, delivered=delivered)

# TODO: Rank system [CHETAN]
@app.route('/volunteerRanking', methods=['GET'])
def volunteerRankingPage():
    return render_template('volunteer_ranking.html')

@app.route('/get_volunteer_ranking', methods=['GET'])
def get_volunteer_ranking():
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    cursor = conn.cursor()

    # get donation count
    cursor.execute('''
        SELECT p.userName, p.fname, p.lname, COUNT(d.orderID) AS deliveries
        FROM Person p 
        JOIN Act a ON p.userName = a.userName
        JOIN Role r ON a.roleID = r.roleID
        JOIN Delivered d ON p.userName = d.userName
        WHERE r.rDescription = 'Volunteer'
        AND d.date BETWEEN %s AND %s
        GROUP BY p.userName
        ORDER BY deliveries DESC
    ''', (start, end))
    ranking = cursor.fetchall()
    
    cursor.close()

    return render_template('volunteer_ranking.html', ranking=ranking)

# TODO: Update enabled [CHETAN]
@app.route('/deliveryStatus', methods=['GET'])
def updatePage():
    return render_template('/delivery_status.html')

@app.route('/update_status', methods=['GET', 'POST'])
def update_delivery_status():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        orderID = request.form.get('orderID')
        newStatus = request.form.get('newStatus')
        username = session['username']
        
        if not orderID or not newStatus:
            return redirect(url_for('updatePage'))
        
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 1 
            FROM Delivered
            WHERE orderID = %s AND userName = %s
        ''', (orderID, username))
        is_deliverer = cursor.fetchone() is not None

        cursor.execute('''
            SELECT 1
            FROM Ordered
            WHERE orderID = %s AND supervisor = %s
        ''', (orderID, username))
        is_supervisor = cursor.fetchone() is not None

        if not (is_deliverer or is_supervisor):
            flash("Unauthorized.")
            return redirect(url_for('updatePage'))

        cursor.execute('''
            UPDATE Delivered
            SET status = %s
            WHERE orderID = %s
            AND (userName = %s OR %s IN (
                SELECT supervisor FROM Ordered WHERE orderID = %s
            ))
        ''', (newStatus, orderID, username, username, orderID))
        conn.commit()

        if cursor.rowcount > 0:
            flash("Delivery status updated successfully.")
        else:
            flash("No matching order found or no permission to update.")
        conn.close()

        return redirect(url_for('updatePage'))

    return render_template('delivery_status.html')


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)

