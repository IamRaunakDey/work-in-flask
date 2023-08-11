from flask import *
app = Flask(__name__)
import sqlite3
from tabulate import tabulate



conn = sqlite3.connect('registration.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS registrations
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, gender TEXT, country TEXT)''')


conn.commit()

# @app.route('/')
# def base():
#     return "<h1>GO TO HOME PAGE</h1><a href='{{url_for('home') }}'>HOME PAGE</a>"

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')





@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/get_data')
def get_data():
    conn = sqlite3.connect('registration.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registrations")
    data = cursor.fetchall()   
    conn.close()
   
    # data = []
    # for row in rows:
    #     data.append({
    #         'id': row[0],
    #         'username': row[1],
    #         'email': row[2],
    #         'gender': row[4],
    #         'country': row[5]
    #     })
    
    return jsonify(data)


    


@app.route('/success')
def success():
    return "<h1>Registration Successful</h1></h2>please login through login page"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('registration.db')
    return g.db

# Define a function to close the database connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']

        try:
            db = get_db()
            cursor = db.cursor()

            # Data inserting
            cursor.execute("INSERT INTO registrations (username, email, password, gender, country) VALUES (?, ?, ?, ?, ?)",
                           (username, email, password, gender, country))
            db.commit()

            return redirect(url_for('success'))

        except sqlite3.Error as e:
            # Handle database error
            print("Database error:", e)
            db.rollback()

        finally:
            close_db()

    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug= True,port=5000)