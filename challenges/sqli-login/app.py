from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    # Insert test users
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES ('admin', 'supersecret123', 1)")
    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES ('guest', 'guest', 0)")
    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES ('cat', 'meow123', 0)")
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🐱 Cat Bank Login</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .login-container { 
                background: rgba(255,255,255,0.9); 
                padding: 40px; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                text-align: center;
                min-width: 400px;
            }
            .cat-header { color: #ff6b6b; margin-bottom: 30px; }
            input[type="text"], input[type="password"] { 
                width: 80%; 
                padding: 15px; 
                margin: 10px 0; 
                border: 2px solid #ff9a9e; 
                border-radius: 10px;
                font-size: 16px;
            }
            .login-btn { 
                padding: 15px 30px; 
                background: #ff6b6b; 
                color: white; 
                border: none; 
                cursor: pointer; 
                border-radius: 10px;
                font-size: 18px;
                margin-top: 20px;
                width: 88%;
            }
            .login-btn:hover { background: #ff5252; }
        </style>
        <script>
            console.log("🐱 Welcome to Cat Bank - Ultra Secure Login!");
            console.log("💡 SQL Injection Hint: Try ' OR '1'='1' -- as username");
            console.log("🎭 Fun fact: Cats don't understand SQL... but you do!");
        </script>
    </head>
    <body>
        <div class="login-container">
            <div class="cat-header">
                <h1>🐱 Cat Bank</h1>
                <p><strong>"Where your fish savings are safe!"</strong></p>
                <p>🎬 <em>"Purrfectly secure since 1337!"</em></p>
            </div>
            
            <form method="POST" action="/sqli-login/login">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="login-btn">🐾 Login to Cat Bank</button>
            </form>
            
            <div style="margin-top: 30px; font-size: 14px; color: #666;">
                <p>🔍 <em>Try: guest/guest or admin/supersecret123</em></p>
                <p>🕵️ <em>Or maybe something more... creative?</em></p>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE SQL QUERY - DO NOT USE IN PRODUCTION!
    query = f"SELECT username, is_admin FROM users WHERE username = '{username}' AND password = '{password}'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            username, is_admin = result
            if is_admin:
                flag = "nulleec{sqli_1s_0ld_but_g0ld}"
                return render_template_string('''
                <html>
                <body style="font-family: Arial; text-align: center; background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center;">
                    <div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px;">
                        <h1>🎉 Welcome Admin Cat!</h1>
                        <div style="background: #28a745; color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                            <h2>🏆 Admin Flag Captured!</h2>
                            <p><strong>{{ flag }}</strong></p>
                        </div>
                        <p>🐱 You've successfully performed SQL injection!</p>
                        <p>🎭 Even cats can be hackers!</p>
                        <a href="/sqli-login/" style="color: #ff6b6b;">← Back to Login</a>
                    </div>
                </body>
                </html>
                ''', flag=flag)
            else:
                return render_template_string('''
                <html>
                <body style="font-family: Arial; text-align: center; background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center;">
                    <div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px;">
                        <h1>🐱 Welcome {{ username }}!</h1>
                        <p>You're logged in as a regular cat user.</p>
                        <p>🔒 No admin privileges = No flag for you!</p>
                        <a href="/sqli-login/" style="color: #ff6b6b;">← Back to Login</a>
                    </div>
                </body>
                </html>
                ''', username=username)
        else:
            return render_template_string('''
            <html>
            <body style="font-family: Arial; text-align: center; background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center;">
                <div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px;">
                    <h1>🚫 Login Failed!</h1>
                    <p>Invalid credentials, silly cat!</p>
                    <a href="/sqli-login/" style="color: #ff6b6b;">← Try Again</a>
                </div>
            </body>
            </html>
            ''')
    
    except sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)