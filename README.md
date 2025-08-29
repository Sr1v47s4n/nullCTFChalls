# 🎯 CTF Challenge Suite

A comprehensive collection of beginner-friendly and advanced CTF challenges featuring fun memes, cats, and Hollywood references! All challenges are ethical, self-contained, and safe for educational purposes.

## 🚀 Quick Start

1. **Start the CTF Suite:**
   ```bash
   chmod +x start_ctf.sh
   ./start_ctf.sh
   ```

2. **Access the CTF Hub:**
   Open your browser to `http://localhost`

## 🎮 Challenges

### 🟢 Beginner Challenges

1. **🐱 Flask SSRF** - `http://localhost/flask-ssrf/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{c0ngr4ts_f0r_f7nd1ngs_33rf}`
   - **Hint:** Cats don't allow outsiders, but maybe insiders can sneak in!

2. **🦸‍♂️ FastAPI XSS** - `http://localhost/fastapi-xss/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{x5s_1s_funny_r1ght}`
   - **Hint:** This site is so safe, even Thanos can't break it!

3. **📝 JS Todo IDOR** - `http://localhost/js-todo-idor/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{1d0r_4lw4ys_h1dd3n}`
   - **Hint:** Even cats need to stay organized... or do they?

4. **🎬 Client-Side Login** - `http://localhost/client-side-login/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{cl13nt_s1d3_ch3at_w1ns}`
   - **Hint:** In Hollywood, you can be anything... even admin!

5. **🕶️ Telnet Buffer Overflow** - `telnet localhost 5005`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{buff3r_0v3rfl0w_w0w}`
   - **Hint:** You've broken into the Matrix. Neo is impressed.

6. **🐱 SQL Injection** - `http://localhost/sqli-login/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{sqli_1s_0ld_but_g0ld}`
   - **Hint:** Where your fish savings are safe... or are they?

7. **🏓 Command Injection** - `http://localhost/cmd-injection/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{c0mm4nd_1nj3ct10n}`
   - **Hint:** Ping like a cat - fast and precise!

8. **🔐 Basic Crypto** - `http://localhost/basic-crypto/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{cryp70_b4by}`
   - **Hint:** Where cats learn the ancient art of secret messages!

9. **📸 File Upload** - `http://localhost/file-upload/`
   - **Difficulty:** Easy
   - **Flag:** `nulleec{upl04d3d_f1l3}`
   - **Hint:** Share your cutest cat photos... and more!

### 🔴 Advanced Challenges

10. **🏦 Race Condition** - `http://localhost/race-condition/`
    - **Difficulty:** Hard
    - **Flag:** `nulleec{r4c3_c0nd1t10n}`
    - **Hint:** Where fast cats make fast money!

11. **🔐 JWT Forgery** - `http://localhost/jwt-forgery/`
    - **Difficulty:** Hard
    - **Flag:** `nulleec{jwt_f0rg3ry_m45t3r}`
    - **Hint:** Ultra-secure JWT authentication... or is it?

## 🛠️ Technical Details

### Architecture
- **Docker Compose:** Multi-container setup
- **Nginx:** Reverse proxy and load balancer
- **Python Flask/FastAPI:** Backend services
- **HTML/CSS/JavaScript:** Frontend challenges
- **SQLite:** Database for vulnerable apps

### Security Features
- All challenges run in isolated Docker containers
- Rate limiting implemented in Nginx
- Safe for localhost deployment
- No actual malicious code

### Fun Elements
- 🐱 Cat memes and references throughout
- 🎬 Hollywood movie quotes and themes
- 🎭 Tamil culture references (in English)
- Console hints and Easter eggs
- Decoy endpoints and fake hints

## 📋 Solution Hints

### General Tips
1. Always check the browser console for hints
2. Look at `robots.txt` files
3. Inspect network requests in DevTools
4. Try common payloads and techniques
5. Read the memes - they often contain real hints!

### Specific Hints
- **SSRF:** Check console logs and robots.txt for endpoint clues
- **XSS:** Try script tags in the name parameter
- **IDOR:** Change user_id parameter in URL
- **Client-Side:** Modify the response object in DevTools
- **Buffer Overflow:** Numbers greater than 1337
- **SQLi:** Classic `' OR '1'='1' --` injection
- **Command Injection:** Use `;` or `&&` to chain commands
- **Crypto:** ROT13 cipher (shift by 13)
- **File Upload:** Double extensions like `.php.jpg`
- **Race Condition:** Send multiple requests simultaneously
- **JWT:** Weak secret key is "secret"

## 🔧 Troubleshooting

### Port Conflicts
If ports are already in use, modify the `docker-compose.yml` file:
```yaml
ports:
  - "8080:80"  # Change from 80:80
```

### Container Issues
```bash
# Restart all services
docker-compose down
docker-compose up -d --build

# View logs
docker-compose logs [service-name]
```

### Cleanup
```bash
# Stop and remove all containers
docker-compose down

# Remove images
docker-compose down --rmi all
```

## 🎓 Educational Use

This CTF suite is designed for:
- Security education and training
- Ethical hacking practice
- Web application security learning
- CTF competition preparation

## ⚠️ Disclaimer

These challenges contain intentionally vulnerable code for educational purposes only. **Never deploy these applications in production or on public networks.** Always practice ethical hacking and obtain proper authorization before testing security vulnerabilities.

## 🎉 Have Fun!

Remember: Every flag follows the format `nulleec{...}` and contains fun references to cats, movies, and memes. Happy hacking! 🐱