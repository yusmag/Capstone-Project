from flask import Flask, render_template_string

app = Flask(__name__)

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>This Side Up | Skimboards</title>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Righteous&display=swap" rel="stylesheet">
  <style>

    body, p, .nav-links a, button, .icon-btn, .hero p {
      font-family: 'Righteous', cursive;
    }

    body {
      background: #F4F4F4;
      margin: 0;
    }

    /* NAVBAR */
    .navbar {
      background: #000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 18px 32px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    .nav-left {
      display: flex;
      align-items: center;
      gap: 32px;
    }

    .logo {
      display: flex;
      align-items: center;
      height: 50px;     
    }

    .logo-img {
      height: 38px;     
      width: auto;
      display: block;
    }

    .nav-links a {
      text-decoration: none;
      color: #fff;
      margin-right: 20px;
      font-size: 24px;
    }

    .nav-links a:hover {
      color: #F46A3D;
    }

    /* ICONS */
    .nav-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .icon-btn {
      background: #fff;
      border: 2px solid #222;
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 24px;
      cursor: pointer;
      transition: 0.2s;
    }

    .icon-btn:hover {
      background: #f3f3f3;
      transform: translateY(-1px);
    }

    /* HERO */
    .hero {
      position: relative;
      text-align: center;
      padding: 100px 20px;
      background: url('/static/bg/hero.jpg') no-repeat right center;
      background-size: cover;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .hero h1 {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 100px;
      color: #000;
      margin-bottom: 10px;
    }

    .hero p {
      color: #444;
      margin-bottom: 30px;
      font-size: 20px;
    }

    .hero-buttons button {
      background: #F46A3D;
      color: #fff;
      border: none;
      padding: 16px 32px;
      margin: 0 10px;
      cursor: pointer;
      font-weight: bold;
      font-size: 20px;
      transition: background 0.2s;
    }

    .hero-buttons button:hover {
      background: #333;
    }

  </style>
</head>
<body>

  <!-- NAVBAR -->
  <header class="navbar">
    <div class="nav-left">
      <div class="logo">
        <img src="/static/logo/logo.jpg" class="logo-img" alt="This Side Up Logo">
      </div>
      <nav class="nav-links">
        <a href="/">Shop</a>
        <a href="/about">About</a>
        <a href="/community">Community</a>
      </nav>
    </div>

    <div class="nav-right">
      <button class="icon-btn">🔍</button>
      <button class="icon-btn">🛒</button>
      <button class="icon-btn" onclick="location.href='/user'">👤</button>
    </div>
  </header>

  <!-- HERO -->
  <section class="hero">
    <div class="hero-text">
      <h1>Welcome to This Side Up</h1>
      <p>Dedicated to bringing the thrill of Skimboarding</p>
      <div class="hero-buttons">
        <button>OUR SKIMBOARDS</button>
        <button>BOARD BUYERS GUIDE</button>
      </div>
    </div>
  </section>

</body>
</html>
"""

USER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>User Login | This Side Up</title>

  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Righteous&display=swap" rel="stylesheet">

  <style>

    body, p, .nav-links a, button {
      font-family: 'Righteous', cursive;
    }

    body {
      background: #D9D9D9;
      margin: 0;
    }

    /* NAVBAR */
    .navbar {
      background: #000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 18px 32px;
    }

    .nav-left {
      display: flex;
      align-items: center;
      gap: 32px;
    }

    .logo-img {
      height: 38px;
    }

    .nav-links a {
      text-decoration: none;
      color: #fff;
      margin-right: 20px;
      font-size: 24px;
    }

    .nav-links a:hover {
      color: #F46A3D;
    }

    /* ICON BUTTONS */
    .nav-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .icon-btn {
      background: #fff;
      border: 2px solid #222;
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 22px;
      cursor: pointer;
    }

    /* LOGIN FORM */
    .login-container {
      width: 420px;
      margin: 80px auto;
    }

    .login-container label {
      font-size: 18px;
      margin-bottom: 6px;
      display: block;
      color: #000;
    }

    .login-container input {
      width: 100%;
      padding: 10px;
      font-size: 16px;
      border: 2px solid #888;
      background: #e9e9e9;
      margin-bottom: 25px;
    }

    .helper-text {
      font-size: 12px;
      text-align: right;
      margin-top: -18px;
      margin-bottom: 20px;
      color: #000;
    }

    .btn-row {
      display: flex;
      align-items: center;
      gap: 20px;
      margin-top: 10px;
    }

    .login-btn {
      background: #A5A5A5;
      border: none;
      padding: 12px 26px;
      color: #fff;
      cursor: pointer;
      font-size: 16px;
    }

    .create-btn {
      background: transparent;
      border: none;
      color: #000;
      cursor: pointer;
      font-size: 16px;
    }

  </style>
</head>

<body>

  <!-- NAVBAR -->
  <header class="navbar">
    <div class="nav-left">
      <div class="logo">
        <img src="/static/logo/logo.jpg" class="logo-img">
      </div>
      <nav class="nav-links">
        <a href="/">Shop</a>
        <a href="/about">About</a>
        <a href="/community">Community</a>
      </nav>
    </div>

    <div class="nav-right">
      <button class="icon-btn">🔍</button>
      <button class="icon-btn">🛒</button>
      <button class="icon-btn" onclick="location.href='/user'">👤</button>
    </div>
  </header>

  <!-- LOGIN FORM -->
  <div class="login-container">
    <label>Email</label>
    <input type="email" placeholder="Enter your email">

    <label>Password</label>
    <input type="password" placeholder="Enter your password">

    <div class="helper-text">Forgot your password?</div>

    <div class="btn-row">
      <button class="login-btn">SIGN IN</button>
      <button class="create-btn">CREATE ACCOUNT</button>
    </div>
  </div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/user")
def user():
    return render_template_string(USER_HTML)

if __name__ == "__main__":
    app.run(debug=True)
