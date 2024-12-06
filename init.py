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

# TODO: Accept donation [ELI]

# TODO: Start an order [IAN]

# TODO: Add to current order [IAN]

# TODO: Prepare order [IAN]

# TODO: User's tasks [CHETAN]

# TODO: Rank system [CHETAN]

# TODO: Update enabled [CHETAN]


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)

