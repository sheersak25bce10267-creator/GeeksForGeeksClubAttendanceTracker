from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS participants (id TEXT PRIMARY KEY, name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM participants")
    participants = c.fetchall()
    
    total_present = sum(1 for p in participants if p[2] == 'Present')
    total_absent = len(participants) - total_present
    
    return render_template('index.html', participants=participants, present=total_present, absent=total_absent)

@app.route('/add', methods=['POST'])
def add():
    p_id = request.form['participant_id']
    name = request.form['name']
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO participants (id, name, status) VALUES (?, ?, ?)", 
              (p_id, name, 'Absent'))
    conn.commit()
    return redirect('/')

@app.route('/update/<p_id>/<status>')
def update(p_id, status):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("UPDATE participants SET status = ? WHERE id = ?", (status, p_id))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)