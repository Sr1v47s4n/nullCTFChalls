from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Weak secret key - DO NOT USE IN PRODUCTION!
SECRET_KEY = "secret"
ALGORITHM = "HS256"

users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
    "cat": {"password": "meow", "role": "user"}
}

def create_jwt_token(username: str, role: str):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

@app.get("/", response_class=HTMLResponse)
async def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔐 JWT Cat Security</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }
            .jwt-container { 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 20px; 
                backdrop-filter: blur(20px);
                text-align: center;
                min-width: 500px;
                box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            }
            .jwt-header { 
                color: #ffd700; 
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                margin-bottom: 30px;
            }
            input[type="text"], input[type="password"] { 
                width: 80%; 
                padding: 15px; 
                margin: 10px 0; 
                border: none; 
                border-radius: 10px;
                font-size: 16px;
            }
            .login-btn { 
                padding: 15px 30px; 
                background: #ff6b35; 
                color: white; 
                border: none; 
                cursor: pointer; 
                border-radius: 10px;
                font-size: 18px;
                margin-top: 20px;
                width: 88%;
            }
            .login-btn:hover { background: #e55a2b; }
        </style>
        <script>
            console.log("🔐 Welcome to JWT Cat Security!");
            console.log("💡 JWT Forgery Hint: The secret key is very weak - try 'secret'");
            console.log("🐱 Use jwt.io to decode and forge tokens!");
            console.log("🎭 Change the role to 'admin' and re-encode with the weak secret!");
            console.log("🔧 Try logging in as: cat/meow or user/user123");
        </script>
    </head>
    <body>
        <div class="jwt-container">
            <div class="jwt-header">
                <h1>🔐 JWT Cat Security</h1>
                <p><strong>"Ultra-secure JWT authentication!"</strong></p>
                <p>🎬 <em>"Our tokens are unbreakable... or are they?"</em></p>
            </div>
            
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="login-btn">🐾 Login with JWT!</button>
            </form>
            
            <div style="margin-top: 30px; font-size: 14px; opacity: 0.8;">
                <p>🔍 <em>Try: cat/meow, user/user123, admin/admin123</em></p>
                <p>🕵️ <em>Or forge your own JWT token with admin role!</em></p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = users_db.get(username)
    
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt_token(username, user["role"])
    
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="jwt_token", value=token, httponly=True)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    token = request.cookies.get("jwt_token")
    
    if not token:
        return RedirectResponse(url="/")
    
    payload = verify_jwt_token(token)
    
    if not payload:
        return RedirectResponse(url="/")
    
    username = payload.get("username")
    role = payload.get("role")
    
    flag_content = ""
    if role == "admin":
        flag_content = '''
        <div style="background: #28a745; color: white; padding: 20px; border-radius: 15px; margin: 20px 0; animation: glow 2s infinite;">
            <h2>🏆 Admin Flag Captured!</h2>
            <p><strong>nulleec{jwt_f0rg3ry_m45t3r}</strong></p>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎛️ JWT Dashboard</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: white;
            }}
            .dashboard-container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 40px; 
                border-radius: 20px; 
                backdrop-filter: blur(20px);
            }}
            .jwt-token {{
                background: #000;
                color: #00ff00;
                padding: 20px;
                border-radius: 10px;
                font-family: monospace;
                word-break: break-all;
                margin: 20px 0;
                font-size: 14px;
            }}
            @keyframes glow {{
                0% {{ box-shadow: 0 0 20px #28a745; }}
                50% {{ box-shadow: 0 0 40px #28a745, 0 0 60px #28a745; }}
                100% {{ box-shadow: 0 0 20px #28a745; }}
            }}
        </style>
        <script>
            console.log("🎛️ JWT Dashboard loaded!");
            console.log("🔍 Your current JWT token is visible below");
            console.log("💡 Try decoding it at jwt.io and changing the role to 'admin'");
            console.log("🛠️ Then replace your cookie with the forged token!");
        </script>
    </head>
    <body>
        <div class="dashboard-container">
            <h1 style="text-align: center; color: #ffd700;">🎛️ JWT Dashboard</h1>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>👤 User Information</h3>
                <p><strong>Username:</strong> {username}</p>
                <p><strong>Role:</strong> {role}</p>
                <p><strong>Token Algorithm:</strong> HS256</p>
                <p><strong>Secret Key Hint:</strong> 🤫 Very common word...</p>
            </div>
            
            {flag_content}
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h3>🔐 Your JWT Token:</h3>
                <div class="jwt-token">{token}</div>
                <p style="font-size: 12px; opacity: 0.8;">Copy this token to jwt.io to decode and modify it!</p>
            </div>
            
            {'' if role == 'admin' else '''
            <div style="text-align: center; margin-top: 30px;">
                <p>🔒 You need admin role to see the flag!</p>
                <p>💡 Try forging a JWT token with role = "admin"</p>
            </div>
            '''}
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="/logout" style="color: #ff6b35; text-decoration: none; font-weight: bold;">🚪 Logout</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("jwt_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)