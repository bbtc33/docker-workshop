from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)



# Database connection configuration
db_config = {
    'host': 'db',  # The name of the service in docker-compose.yml
    'user': 'root',  # Default user for MariaDB
    'password': 'root_password',  # Change this to your desired password
    'database': 'notes_db'
}

# Route to display all notes
@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', notes=notes)

# Route to create a new note
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')
    return render_template('create.html')

# Route to view a single note
@app.route('/note/<int:id>')
def note_detail(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE id = %s", (id,))
    note = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('note_detail.html', note=note)

# Function to initialize the database schema
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        content TEXT NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Initialize the database before the first request
@app.before_first_request
def setup():
    init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
