from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, name: str = ""):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "name": name,
        "flag": "nulleec{x5s_1s_funny_r1ght}" if "<script>" in name.lower() else ""
    })

@app.get("/robots.txt")
async def robots():
    return """User-agent: *
Disallow: /admin
Disallow: /flag

# 🦸‍♂️ Thanos says: "This site is perfectly balanced... or is it?"
# Hint: Sometimes the name parameter can be more than just a name!
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)