from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

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

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)

