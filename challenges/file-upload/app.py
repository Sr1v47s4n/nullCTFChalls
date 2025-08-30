from flask import Flask, request, render_template_string, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📸 Cat Photo Gallery</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(45deg, #ff9a56, #ffad56, #ffc356, #ffd756);
                background-size: 400% 400%;
                animation: gradient 10s ease infinite;
                min-height: 100vh;
                padding: 20px;
            }
            @keyframes gradient { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
            .gallery-container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.9); 
                padding: 40px; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            }
            .upload-area {
                border: 3px dashed #ff9a56;
                padding: 40px;
                text-align: center;
                border-radius: 15px;
                margin: 20px 0;
                background: rgba(255,154,86,0.1);
            }
            input[type="file"] { 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
                font-size: 16px;
            }
            .upload-btn { 
                padding: 15px 30px; 
                background: #ff6b6b; 
                color: white; 
                border: none; 
                cursor: pointer; 
                border-radius: 10px;
                font-size: 18px;
                margin-top: 15px;
            }
            .file-list {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            .file-item {
                padding: 10px;
                margin: 5px 0;
                background: white;
                border-radius: 5px;
                border-left: 4px solid #28a745;
            }
        </style>
        <script>
            console.log("📸 Welcome to Cat Photo Gallery!");
            console.log("💡 File Upload Hint: Try uploading a .php file disguised as .jpg");
            console.log("🐱 Maybe rename shell.php to shell.php.jpg?");
            console.log("🎭 Cats are masters of disguise!");
        </script>
    </head>
    <body>
        <div class="gallery-container">
            <h1 style="text-align: center; color: #ff6b6b;">📸 Cat Photo Gallery</h1>
            <p style="text-align: center;"><strong>"Share your cutest cat photos!"</strong></p>
            <p style="text-align: center;">🎬 <em>"Every photo tells a story... some tell secrets!"</em></p>
            
            <form method="POST" action="/file-upload/upload" enctype="multipart/form-data">
                <div class="upload-area">
                    <h3>🐱 Upload Your Cat Photo</h3>
                    <p>Accepted formats: JPG, JPEG, PNG, GIF</p>
                    <input type="file" name="file" accept=".jpg,.jpeg,.png,.gif" required>
                    <br>
                    <button type="submit" class="upload-btn">📤 Upload Cat Photo!</button>
                </div>
            </form>
            
            {% if uploaded_files %}
            <div class="file-list">
                <h3>📂 Uploaded Files:</h3>
                {% for file in uploaded_files %}
                <div class="file-item">
                    📁 {{ file }}
                    <a href="/uploads/{{ file }}" target="_blank" style="float: right; color: #007bff;">View</a>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <div style="margin-top: 30px; text-align: center; font-size: 14px; color: #666;">
                <p>🔍 <em>Try uploading: cat.jpg, photo.png</em></p>
                <p>🕵️ <em>Or maybe... something with a double extension?</em></p>
            </div>
        </div>
    </body>
    </html>
    ''', uploaded_files=uploaded_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        
        # Vulnerable: Check only the last extension
        if allowed_file(filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Check if it's a PHP file (for demonstration)
            if filename.lower().endswith('.php.jpg') or '.php' in filename.lower():
                # Create a flag for successful PHP upload
                flag_content = "<?php echo 'nulleec{upl04d3d_f1l3}'; ?>"
                with open(file_path, 'w') as f:
                    f.write(flag_content)
                
                return render_template_string('''
                <html>
                <body style="font-family: Arial; background: linear-gradient(45deg, #ff9a56, #ffad56); min-height: 100vh; padding: 20px;">
                    <div style="background: rgba(255,255,255,0.9); padding: 40px; border-radius: 20px; max-width: 600px; margin: 50px auto; text-align: center;">
                        <h1>🎉 File Upload Successful!</h1>
                        <div style="background: #28a745; color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                            <h2>🏆 Flag Discovered!</h2>
                            <p><strong>nulleec{upl04d3d_f1l3}</strong></p>
                        </div>
                        <p>🐱 You successfully uploaded a PHP file disguised as an image!</p>
                        <p>🎭 File saved as: {{ filename }}</p>
                        <a href="/" style="color: #ff6b6b;">← Back to Gallery</a>
                    </div>
                </body>
                </html>
                ''', filename=filename)
            
            return redirect(url_for('index'))
        else:
            return "File type not allowed! Only JPG, JPEG, PNG, GIF files are accepted."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    return "File not found!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)