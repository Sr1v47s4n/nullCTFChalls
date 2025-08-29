#!/bin/bash

echo "🎯 Starting CTF Challenge Suite..."

# Create necessary directories
mkdir -p challenges/flask-ssrf
mkdir -p challenges/fastapi-xss/templates
mkdir -p challenges/js-todo-idor
mkdir -p challenges/client-side-login
mkdir -p challenges/telnet-bof
mkdir -p challenges/sqli-login
mkdir -p challenges/cmd-injection
mkdir -p challenges/basic-crypto
mkdir -p challenges/file-upload
mkdir -p challenges/race-condition
mkdir -p challenges/jwt-forgery
mkdir -p nginx

echo "📁 Directories created..."

# Build and start all services
echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

echo "⏳ Waiting for services to start..."
sleep 10

echo "🎉 CTF Challenge Suite is ready!"
echo ""
echo "🌟 Access the CTF Hub at: http://localhost"
echo ""
echo "📋 Available Challenges:"
echo "  🐱 Flask SSRF          → http://localhost/flask-ssrf/"
echo "  🦸‍♂️ FastAPI XSS          → http://localhost/fastapi-xss/"
echo "  📝 JS Todo IDOR        → http://localhost/js-todo-idor/"
echo "  🎬 Client-Side Login    → http://localhost/client-side-login/"
echo "  🕶️ Telnet Buffer Overflow → telnet localhost 5005"
echo "  🐱 SQL Injection       → http://localhost/sqli-login/"
echo "  🏓 Command Injection    → http://localhost/cmd-injection/"
echo "  📸 File Upload          → http://localhost/file-upload/"
echo "  🏦 Race Condition (HARD) → http://localhost/race-condition/"
echo "  🔐 JWT Forgery (HARD)    → http://localhost/jwt-forgery/"
echo ""
echo "🎭 All flags follow format: nulleec{...}"
echo "🐱 Have fun and happy hacking!"