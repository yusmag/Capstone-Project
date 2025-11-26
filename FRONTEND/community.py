from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Community Events | This Side Up</title>

  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Righteous&display=swap" rel="stylesheet" />

  <style>
    body {
      margin: 0;
      font-family: 'Righteous', cursive;
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

    .nav-links a {
      text-decoration: none;
      color: #fff;
      margin-right: 20px;
      font-size: 24px;
    }

    .nav-links a:hover {
      color: #F46A3D;
    }

    .icon-btn {
      background: #fff;
      border: 2px solid #222;
      border-radius: 8px;
      padding: 6px 10px;
      font-size: 22px;
      cursor: pointer;
      transition: .2s;
    }
    .icon-btn:hover { background: #f3f3f3; }

    /* PAGE WRAPPER */
    .content-wrapper {
      max-width: 820px;
      margin: 50px auto;
      background: rgba(255,255,255,0.96);
      padding: 40px 60px;
      border-radius: 8px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }

    /* DATE TAG */
    .date-tag {
      background: #F46A3D;
      color: #fff;
      font-size: 14px;
      padding: 6px 16px;
      width: fit-content;
      margin: 0 auto 20px auto;
      border-radius: 4px;
      font-weight: bold;
    }

    /* TITLE */
    .page-title {
      font-family: 'Bebas Neue', sans-serif;
      text-align: center;
      font-size: 42px;
      margin-bottom: 25px;
      letter-spacing: 1px;
    }

    /* EVENT IMAGE */
    .event-img {
      width: 100%;
      border-radius: 4px;
      margin-bottom: 20px;
    }

    /* SUBHEADING */
    .subheading {
      text-align: center;
      font-weight: bold;
      margin: 20px 0;
    }

    /* MAIN TEXT */
    .event-text {
      font-size: 15px;
      line-height: 1.7;
      color: #222;
      margin-bottom: 30px;
    }
  </style>
</head>

<body>

  <!-- NAVBAR -->
  <header class="navbar">
    <div class="nav-left">
      <img src="/static/logo/logo.jpg" class="logo-img" style="height:38px;" />
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

  <!-- BLOG CONTENT -->
  <div class="content-wrapper">

    <div class="date-tag">MARCH 11, 2025</div>

    <h1 class="page-title">Premier Skimboard League – East Coast Park</h1>

    <img src="/static/bg/hero.jpg" class="event-img" />

    <div class="subheading">THIS SIDE UP — WE RIDE!</div>

    <p class="event-text">
      A huge weekend for the local skimboarding community as riders gathered at East Coast Park
      for the 2025 Premier Skimboard League. With perfect weather and a strong turnout,
      competitors battled it out on clean shorebreaks with plenty of fast lines, wraps, and big airs.
    </p>

    <p class="event-text">
      The day started early with warm-ups and practice runs. As the tide filled in, the waves began
      shaping perfectly against the shoreline, giving riders the chance to showcase their best tricks.
      Crowds gathered quickly and the atmosphere turned electric as heats progressed.
    </p>

    <p class="event-text">
      It was an unforgettable event with impressive performances, new friendships, and a strong
      showing of support from the entire skim community. Stay tuned for more events coming soon!
    </p>

  </div>

</body>
</html>
"""

@app.route("/community")
def community():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
