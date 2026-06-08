from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'debate.db'

def get_db():
    """Return database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with participants table"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# ========== ROUTES ==========

@app.route('/')
def home():
    """Home page with navigation"""
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_participant():
    """Register a new participant"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        topic = request.form.get('topic', '').strip()
        
        # Validation
        if not name or len(name) < 2:
            flash('❌ Name must be at least 2 characters', 'danger')
            return redirect('/register')
        
        if not topic or len(topic) < 5:
            flash('❌ Topic must be at least 5 characters', 'danger')
            return redirect('/register')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check for duplicate
        cursor.execute("SELECT id FROM participants WHERE name = ? AND topic = ?", (name, topic))
        if cursor.fetchone():
            flash('⚠️ Participant with same name and topic already exists!', 'warning')
            conn.close()
            return redirect('/register')
        
        cursor.execute("INSERT INTO participants (name, topic) VALUES (?, ?)", (name, topic))
        conn.commit()
        conn.close()
        
        flash(f'✅ {name} registered successfully!', 'success')
        return redirect('/')
    
    return render_template('register.html')

@app.route('/judge', methods=['GET', 'POST'])
def judge_panel():
    """Judge panel to assign scores"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        try:
            participant_id = request.form.get('participant')
            score = int(request.form.get('score', 0))
            judge_name = request.form.get('judge_name', '').strip()
            
            # Validate score range
            if score < 0 or score > 100:
                flash('❌ Score must be between 0 and 100', 'danger')
                return redirect('/judge')
            
            if not judge_name:
                judge_name = "Anonymous Judge"
            
            cursor.execute("UPDATE participants SET score = ? WHERE id = ?", (score, participant_id))
            conn.commit()
            
            flash(f'✅ Score {score} submitted by {judge_name}!', 'success')
            return redirect('/results')
            
        except (ValueError, TypeError):
            flash('❌ Invalid score value', 'danger')
            return redirect('/judge')
        finally:
            conn.close()
    
    cursor.execute("SELECT * FROM participants ORDER BY name")
    participants = cursor.fetchall()
    conn.close()
    return render_template('judge_panel.html', participants=participants)

@app.route('/results')
def show_results():
    """Show leaderboard with rankings"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participants ORDER BY score DESC")
    results = cursor.fetchall()
    
    # Calculate statistics
    total = len(results)
    highest = results[0]['score'] if results else 0
    avg_score = round(sum(r['score'] for r in results) / total, 1) if total > 0 else 0
    
    conn.close()
    return render_template('results.html', results=results, total=total, highest=highest, avg_score=avg_score)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_participant(id):
    """Delete a participant (POST only for security)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM participants WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('🗑️ Participant deleted successfully', 'info')
    return redirect('/results')

# ========== RUN APP ==========
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)