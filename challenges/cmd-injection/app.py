from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏓 Cat Ping Service</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            @keyframes gradient { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
            .ping-container { 
                background: rgba(255,255,255,0.95); 
                padding: 40px; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                text-align: center;
                min-width: 500px;
            }
            input[type="text"] { 
                width: 70%; 
                padding: 15px; 
                margin: 10px; 
                border: 2px solid #4ecdc4; 
                border-radius: 10px;
                font-size: 16px;
            }
            .ping-btn { 
                padding: 15px 30px; 
                background: #ff6b6b; 
                color: white; 
                border: none; 
                cursor: pointer; 
                border-radius: 10px;
                font-size: 18px;
                margin-top: 10px;
            }
            .result { 
                margin-top: 20px; 
                padding: 20px; 
                background: #f8f9fa; 
                border-radius: 10px; 
                text-align: left;
                font-family: monospace;
                white-space: pre-wrap;
                max-height: 300px;
                overflow-y: auto;
            }
        </style>
        <script>
            console.log("🏓 Welcome to Cat Ping Service!");
            console.log("💡 Command Injection Hint: Try 127.0.0.1; ls to list files");
            console.log("🐱 Or maybe: 127.0.0.1 && cat flag.txt");
            console.log("🎭 Cats love to explore... including commands!");
        </script>
    </head>
    <body>
        <div class="ping-container">
            <h1>🏓 Cat Ping Service</h1>
            <p><strong>"Ping like a cat - fast and precise!"</strong></p>
            <p>🎬 <em>"I can ping anything... even other commands!"</em> - Hacker Cat</p>
            
            <form method="POST" action="/ping">
                <input type="text" name="ip" placeholder="Enter IP address (e.g., 127.0.0.1)" required>
                <br>
                <button type="submit" class="ping-btn">🐾 Ping It!</button>
            </form>
            
            <div style="margin-top: 30px; font-size: 14px; color: #666;">
                <p>🔍 <em>Try pinging: 127.0.0.1 or 8.8.8.8</em></p>
                <p>🕵️ <em>Or maybe combine commands with ; or &&</em></p>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.form.get('ip')
    
    # Create flag file
    with open('flag.txt', 'w') as f:
        f.write('nulleec{c0mm4nd_1nj3ct10n}')
    
    try:
        # VULNERABLE COMMAND EXECUTION - DO NOT USE IN PRODUCTION!
        command = f"ping -c 3 {ip}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
        
        return render_template_string('''
        <html>
        <body style="font-family: Arial; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); min-height: 100vh; padding: 20px;">
            <div style="background: rgba(255,255,255,0.95); padding: 40px; border-radius: 20px; max-width: 800px; margin: 0 auto;">
                <h1>🏓 Ping Results</h1>
                <p><strong>Command:</strong> ping -c 3 {{ ip }}</p>
                <div style="background: #000; color: #00ff00; padding: 20px; border-radius: 10px; font-family: monospace; white-space: pre-wrap; margin: 20px 0; max-height: 400px; overflow-y: auto;">{{ output }}</div>
                <a href="/" style="color: #ff6b6b; text-decoration: none; font-weight: bold;">← Back to Ping Service</a>
            </div>
        </body>
        </html>
        ''', ip=ip, output=output)
        
    except subprocess.TimeoutExpired:
        return "Command timed out!"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)