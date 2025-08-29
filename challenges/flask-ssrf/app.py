from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

# Create the flag file
flag_content = "nulleec{c0ngr4ts_f0r_f7nd1ngs_33rf}"
os.makedirs('/tmp/internal', exist_ok=True)
with open('/tmp/internal/flag.txt', 'w') as f:
    f.write(flag_content)

@app.route('/')
def index():
    return render_template_string(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cat URL Fetcher 🐱</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .cat-header { text-align: center; color: #333; }
            input[type="url"] { width: 70%; padding: 10px; margin: 10px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        </style>
        <script>
            console.log("🐱 Meow! The cats are hiding secrets... check /internal/");
            console.log("🕵️ Psst... localhost might know more than external sites!");
        </script>
    </head>
    <body>
        <div class="container">
            <h1 class="cat-header">🐱 Cat URL Fetcher</h1>
            <p><strong>Cats don't allow outsiders, but maybe insiders can sneak in 🐱</strong></p>
            <p>This service fetches URLs for you! Just like how cats fetch... wait, cats don't fetch. Anyway...</p>
            
            <form method="POST" action="/flask-ssrf/fetch">
                <input type="url" name="url" placeholder="Enter a URL to fetch" required>
                <button type="submit">Fetch Like a Cat! 🐾</button>
            </form>
            
            
        </div>
    </body>
    </html>
    """
    )

@app.route('/fetch', methods=['POST'])
def fetch_url():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'})
    
    try:
        response = requests.get(url, timeout=5)
        return render_template_string('''
        <html>
        <body style="font-family: Arial; margin: 40px;">
            <h2>🐱 Fetch Results</h2>
            <p><strong>URL:</strong> {{ url }}</p>
            <p><strong>Status Code:</strong> {{ status_code }}</p>
            <div style="background: #f8f9fa; padding: 15px; margin-top: 20px;">
                <h3>Content:</h3>
                <pre style="white-space: pre-wrap;">{{ content }}</pre>
            </div>
            <a href="/">← Back to Cat Fetcher</a>
        </body>
        </html>
        ''', url=url, status_code=response.status_code, content=response.text[:2000])
    except Exception as e:
        return jsonify({'error': f'Meow! Something went wrong: {str(e)}'})

@app.route('/internal/flag')
def internal_flag():
    # This is the SSRF target
    try:
        with open('/tmp/internal/flag.txt', 'r') as f:
            flag = f.read()
        return f"🎉 Congratulations! You found the hidden flag: {flag}"
    except:
        return "Flag file not found!"

@app.route('/status')
def status():
    return jsonify({
        'status': 'alive',
        'message': '🐱 All cats are accounted for!',
        'hint': 'Cats love to hide in internal places...'
    })

@app.route('/about')
def about():
    return '''
    <h1>🐱 About Our Cats</h1>
    <p>Our cats are very security-conscious. They only allow internal visitors!</p>
    <p>Fun fact: Cats can see things that humans cannot... like hidden endpoints!</p>
    '''

@app.route('/meme')
def meme():
    return '''
    <h1>🐱 Cat Meme of the Day</h1>
    <p><strong>"I can haz internal access?"</strong></p>
    <p>- Every hacker cat ever</p>
    <p>Hint: Maybe try fetching something more... local? 😸</p>
    '''

@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /admin
Disallow: /secret
Disallow: /internal

# 🐱 Cat Secret: First part of hidden endpoint is "http://localhost:5000"
# The cats whisper: "Check the console for the second part!"
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
