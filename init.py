from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import re

def validate_input(input_data):
    """
    Validates user input for XSS and SQL injection prevention.
    :param input_data: The user input to validate.
    :return: (bool, str) - A tuple where the first value is True if valid, False otherwise, and the second value is the sanitized input.
    """
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

    query = 'SELECT * FROM person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))

    data = cursor.fetchone()

    cursor.close()
    if (data):
        session['username'] = username
        return redirect(url_for('home'))
    else:
        error = 'Invalid login'
        return render_template('login.html', error=error)

# TODO: add register
@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
    return

@app.route('/home')
def home():
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

# TODO: Add to current order [IAN]

# TODO: Prepare order [IAN]

# TODO: User's tasks [CHETAN]: show all ordered the current (logged in) user has a relationship with (as a client, volunteer, etc) along with more relevant details
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
    print(username)
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
    print()
    delivered = cursor.fetchall()
    cursor.close()

    print(client, supervisor, volunteer, donated, delivered)

    return render_template('usertasks.html', client=client, supervisor=supervisor, volunteer=volunteer, donated=donated, delivered=delivered)

# TODO: Rank system [CHETAN]

# TODO: Update enabled [CHETAN]


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)

