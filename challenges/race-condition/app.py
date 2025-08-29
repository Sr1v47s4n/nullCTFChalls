from flask import Flask, request, render_template_string, jsonify, session
import time
import threading
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo'

# Global variables to simulate a simple database
user_balance = {'user1': 1000}
transfer_lock = threading.Lock()

@app.route('/')
def index():
    session['user'] = 'user1'  # Auto-login for demo
    balance = user_balance.get('user1', 1000)
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏦 Cat Bank - Money Transfer</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }
            .bank-container { 
                max-width: 600px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 20px; 
                backdrop-filter: blur(20px);
            }
            .balance {
                background: #28a745;
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 24px;
                margin: 20px 0;
            }
            input[type="number"] { 
                width: 200px; 
                padding: 15px; 
                margin: 10px; 
                border: none; 
                border-radius: 10px;
                font-size: 16px;
            }
            .transfer-btn { 
                padding: 15px 30px; 
                background: #ff6b6b; 
                color: white; 
                border: none; 
                cursor: pointer; 
                border-radius: 10px;
                font-size: 18px;
                margin: 10px;
            }
            .race-btn {
                padding: 15px 30px; 
                background: #ffc107; 
                color: black; 
                border: none; 
                cursor: pointer; 
                border-radius: 10px;
                font-size: 18px;
                margin: 10px;
            }
            .flag { 
                background: #28a745; 
                color: white; 
                padding: 20px; 
                border-radius: 15px; 
                font-weight: bold; 
                margin-top: 20px;
                text-align: center;
                animation: glow 2s infinite;
            }
            @keyframes glow {
                0% { box-shadow: 0 0 20px #28a745; }
                50% { box-shadow: 0 0 40px #28a745, 0 0 60px #28a745; }
                100% { box-shadow: 0 0 20px #28a745; }
            }
        </style>
        <script>
            console.log("🏦 Welcome to Cat Bank - Money Transfer System!");
            console.log("💡 Race Condition Hint: Send multiple transfer requests very quickly!");
            console.log("🐱 Try the 'Race Attack' button to exploit the vulnerability!");
            console.log("🎭 Fun fact: Cats are very fast, just like race conditions!");
        </script>
    </head>
    <body>
        <div class="bank-container">
            <h1 style="text-align: center; color: #ffd700;">🏦 Cat Bank Transfer</h1>
            <p style="text-align: center;"><strong>"Where fast cats make fast money!"</strong></p>
            
            <div class="balance">
                💰 Your Balance: ${{ balance }}
            </div>
            
            <div style="text-align: center;">
                <h3>💸 Transfer Money</h3>
                <p>Transfer money to account: <strong>savings_account</strong></p>
                
                <form method="POST" action="/transfer" id="transferForm">
                    <input type="number" name="amount" placeholder="Amount" value="100" min="1" max="1000" required>
                    <br>
                    <button type="submit" class="transfer-btn">💸 Transfer Money</button>
                </form>
                
                <button class="race-btn" onclick="raceAttack()">⚡ Race Attack!</button>
                <p style="font-size: 12px; opacity: 0.8;">Click "Race Attack" to send multiple requests quickly!</p>
            </div>
            
            <div id="result" style="margin-top: 30px;"></div>
            
            <div style="margin-top: 40px; text-align: center; font-size: 14px;">
                <p>🎬 <em>"In racing, timing is everything... especially in race conditions!"</em></p>
                <p>🔍 <em>Hint: If your balance goes above $2000, you've found the flag!</em></p>
            </div>
        </div>

        <script>
            async function raceAttack() {
                const amount = document.querySelector('input[name="amount"]').value || 100;
                
                console.log('🏎️ Starting race attack...');
                
                // Send multiple requests simultaneously
                const promises = [];
                for (let i = 0; i < 10; i++) {
                    const formData = new FormData();
                    formData.append('amount', amount);
                    
                    promises.push(
                        fetch('/transfer', {
                            method: 'POST',
                            body: formData
                        })
                    );
                }
                
                try {
                    const responses = await Promise.all(promises);
                    console.log('🏁 Race attack completed!');
                    
                    // Refresh the page to see new balance
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                    
                    document.getElementById('result').innerHTML = `
                        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; text-align: center;">
                            <h3>⚡ Race Attack Completed!</h3>
                            <p>Sent 10 simultaneous transfer requests!</p>
                            <p>Refreshing to see results...</p>
                        </div>
                    `;
                    
                } catch (error) {
                    console.error('Race attack failed:', error);
                }
            }
        </script>
    </body>
    </html>
    ''', balance=balance)

@app.route('/transfer', methods=['POST'])
def transfer():
    amount = int(request.form.get('amount', 0))
    
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'})
    
    # Vulnerable: Race condition - check balance before acquiring lock
    current_balance = user_balance.get('user1', 1000)
    
    if current_balance < amount:
        return jsonify({'error': 'Insufficient funds'})
    
    # Simulate processing delay
    time.sleep(0.1)  # This delay makes the race condition more exploitable
    
    # This should be inside the lock, but it's not!
    with transfer_lock:
        # Simulate the transfer
        user_balance['user1'] -= amount
        # In a real system, we'd add to the destination account
    
    new_balance = user_balance.get('user1', 0)
    
    # Check if race condition was exploited
    if new_balance > 2000:
        return render_template_string('''
        <html>
        <body style="font-family: Arial; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); min-height: 100vh; padding: 20px;">
            <div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px; max-width: 600px; margin: 50px auto; text-align: center;">
                <h1>🎉 Race Condition Exploited!</h1>
                <div class="flag" style="background: #28a745; color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h2>🏆 Flag Captured!</h2>
                    <p><strong>nulleec{r4c3_c0nd1t10n}</strong></p>
                </div>
                <p>🐱 Your balance: ${{ balance }}</p>
                <p>🏎️ You successfully exploited the race condition!</p>
                <p>💡 Multiple transfers were processed simultaneously!</p>
                <a href="/" style="color: #4facfe;">← Back to Bank</a>
            </div>
        </body>
        </html>
        ''', balance=new_balance)
    
    return jsonify({
        'success': True,
        'message': 'Transfer completed',
        'new_balance': new_balance
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)