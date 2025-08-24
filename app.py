from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('debate.db')
    cur = conn.cursor() #act as a remote control, you use to send SQL commands to your database.
    cur.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Home Page
@app.route('/') #flask route decorator
def home():
    return render_template('home.html')

# Register Participant Page
@app.route('/register', methods=['GET', 'POST'])
def register_participant():
    if request.method == 'POST':
        name = request.form['name']
        topic = request.form['topic']
        conn = sqlite3.connect('debate.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO participants (name, topic) VALUES (?, ?)", (name, topic))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('register.html')

# Judge Panel (GET + POST)
@app.route('/judge', methods=['GET', 'POST'])
def judge_panel():
    conn = sqlite3.connect('debate.db')
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            participant_id = request.form['participant']
            score = int(request.form['score'])
            cur.execute("UPDATE participants SET score = ? WHERE id = ?", (score, participant_id))
            conn.commit()
            conn.close()
            return redirect('/results')
        except Exception as e:
            conn.close()
            return f"<h4>Error: {e}</h4><a href='/judge'>Back to Judge Panel</a>"

    cur.execute("SELECT * FROM participants")
    participants = cur.fetchall()
    conn.close()
    return render_template('judge_panel.html', participants=participants)

#  Results Page
@app.route('/results')
def show_results():
    conn = sqlite3.connect('debate.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM participants ORDER BY score DESC")
    results = cur.fetchall()
    conn.close()
    return render_template('results.html', results=results)

# Delete Participant
@app.route('/delete/<int:id>')
def delete_participant(id):
    conn = sqlite3.connect('debate.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM participants WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/results')

#  Start Flask server
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
