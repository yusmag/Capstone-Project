from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
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
      margin: 0;
      background: url('/static/bg/hero.jpg') no-repeat center center fixed;
      background-size: cover;
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
      transition: 0.2s;
    }

    .icon-btn:hover {
      background: #f3f3f3;
      transform: translateY(-1px);
    }

    /* LOGIN BOX */
    .center-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      height: calc(100vh - 100px);
      padding-top: 40px;
    }

    .login-card {
      width: 480px;
      background: rgba(255,255,255,0.92);
      padding: 40px 80px 40px 55px;
      border-radius: 8px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }

    .login-card label {
      font-size: 20px;
      margin-bottom: 10px;
      display: block;
      color: #000;
    }

    .login-card input {
      width: 100%;
      padding: 14px;
      font-size: 16px;
      border: 2px solid #888;
      background: #efefef;
      margin-bottom: 24px;
      border-radius: 4px;
    }

    /* FORGOT PASSWORD – nicely aligned under password field */
    .forgot-row {
      width: 100%;
      display: flex;
      justify-content: flex-end;
      padding-right: 4px;       /* pulls it slightly away from card edge */
      margin-top: -12px;        /* tucks it closer to the password box */
      margin-bottom: 24px;
    }

    .forgot-row a {
      font-size: 13px;
      text-decoration: none;
      color: #000;
    }

    .forgot-row a:hover {
      color: #F46A3D;
    }

    /* BUTTONS */
    .btn-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
    }

    .login-btn,
    .create-btn {
      background: #F46A3D;
      border: none;
      padding: 14px 40px;
      color: #fff;
      cursor: pointer;
      font-size: 18px;
      font-weight: bold;
      border-radius: 4px;
      transition: background 0.2s;
    }

    .login-btn:hover,
    .create-btn:hover {
      background: #333;
    }

  </style>
</head>

<body>

  <!-- NAVBAR -->
  <header class="navbar">
    <div class="nav-left">
      <div class="logo">
        <img src="/static/logo/logo.jpg" class="logo-img" alt="TSU Logo">
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
      <button class="icon-btn">👤</button>
    </div>
  </header>

  <!-- LOGIN CENTERED -->
  <div class="center-wrapper">

    <div class="login-card">
      <label>Email</label>
      <input type="email" placeholder="Enter your email">

      <label>Password</label>
      <input type="password" placeholder="Enter your password">

      <div class="forgot-row">
        <a href="#">Forgot your password?</a>
      </div>

      <div class="btn-row">
        <button class="login-btn">SIGN IN</button>
        <button class="create-btn">CREATE ACCOUNT</button>
      </div>
    </div>

  </div>

</body>
</html>
"""

@app.route("/user")
def user():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
