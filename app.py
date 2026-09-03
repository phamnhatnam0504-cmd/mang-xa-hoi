from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- TỰ ĐỘNG TẠO DATABASE KHI CHẠY APP ---
def init_db():
    conn = sqlite3.connect('dulieu.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            content TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- TRANG CHỦ - ĐỌC VÀ HIỂN THỊ BÀI VIẾT ---
@app.route('/')
def index():
    conn = sqlite3.connect('dulieu.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY id DESC')
    all_posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=all_posts)

# --- XỬ LÝ KHI NGƯỜI DÙNG BẤM NÚT ĐĂNG BÀI ---
@app.route('/dang-bai', methods=['POST'])
def dang_bai():
    user = request.form['user']
    content = request.form['content']
    time_now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    
    conn = sqlite3.connect('dulieu.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (username, content, timestamp) VALUES (?, ?, ?)', (user, content, time_now))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(port=8080)



