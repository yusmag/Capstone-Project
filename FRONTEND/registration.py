from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Create Account | This Side Up</title>

<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Righteous&display=swap" rel="stylesheet">

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

.logo-img {
    height: 38px;
    width: auto;
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 32px;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 26px;
}

.nav-links a {
    text-decoration: none;
    color: #fff;
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

/* PAGE WRAPPER */
.form-wrapper {
    max-width: 600px;
    margin: 60px auto;
    background: rgba(255,255,255,0.96);
    padding: 40px 50px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
}

/* FORM TITLE */
.form-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 48px;
    text-align: center;
    margin-bottom: 25px;
}

/* AVATAR PREVIEW */
.avatar-preview {
    width: 150px;
    height: 150px;
    margin: 0 auto 20px auto;
    border-radius: 50%;
    border: 3px solid #F46A3D;
    object-fit: cover;
    display: block;
}

/* INPUT LABELS */
label {
    font-size: 18px;
    display: block;
    margin-bottom: 6px;
}

/* INPUT FIELDS */
input[type="text"],
input[type="email"],
input[type="password"],
input[type="file"] {
    width: 100%;
    padding: 12px;
    margin-bottom: 22px;
    font-size: 16px;
    border: 2px solid #888;
    background: #efefef;
    border-radius: 4px;
}

/* BUTTON */
.register-btn {
    width: 100%;
    background: #F46A3D;
    border: none;
    padding: 16px;
    font-size: 22px;
    color: #fff;
    font-weight: bold;
    cursor: pointer;
    border-radius: 6px;
    transition: 0.2s;
}

.register-btn:hover {
    background: #333;
}

</style>

<script>
function previewImage(event) {
    const img = document.getElementById('avatarPreview');
    const file = event.target.files[0];

    if (file) {
        img.src = URL.createObjectURL(file);
    }
}
</script>

</head>

<body>

<header class="navbar">
    <div class="nav-left">
        <img src="/static/logo/logo.jpg" class="logo-img" alt="TSU Logo">
        <nav class="nav-links">
            <a href="/">Shop</a>
            <a href="/about">About</a>
            <a href="/community">Community</a>
            <a href="/user">Login</a>
        </nav>
    </div>

    <div class="nav-right">
        <button class="icon-btn">🔍</button>
        <button class="icon-btn">🛒</button>
        <button class="icon-btn">👤</button>
    </div>
</header>

<div class="form-wrapper">

    <h1 class="form-title">Create Account</h1>

    <!-- Avatar Preview -->
    <img id="avatarPreview" src="/static/avatar.jpg" class="avatar-preview">

    <label>Upload Selfie</label>
    <input type="file" accept="image/*" onchange="previewImage(event)">

    <label>First Name</label>
    <input type="text" placeholder="Enter first name">

    <label>Last Name</label>
    <input type="text" placeholder="Enter last name">

    <label>Email</label>
    <input type="email" placeholder="Enter your email">

    <label>Password</label>
    <input type="password" placeholder="Enter your password">

    <label>Address</label>
    <input type="text" placeholder="Enter your address">

    <button class="register-btn">REGISTER</button>

</div>

</body>
</html>
"""

@app.route("/registration")
def registration():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
