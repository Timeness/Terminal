from flask import Flask, request, render_template, jsonify, session
import io, contextlib, traceback, logging
from flask_cors import CORS
import requests
import secrets

myhexs = secrets.token_hex(32)

app = Flask(__name__)
app.secret_key = myhexs
CORS(app)

allowed_users = ["6505111743", "6517565595", "5896960462", "5220416927"]  # allowed Telegram user IDs

# logging.basicConfig(filename='access_log.txt', level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth-telegram', methods=['POST'])
def telegram_auth():
    data = request.json
    user = data.get('user')

    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    # logging.info(f"[LOGIN] User: {user.get('id')} | IP: {ip} | UA: {ua}")

    session['user_id'] = str(user.get('id'))
    allowed = str(user.get('id')) in allowed_users
    return jsonify({"allowed": allowed})

@app.route('/eval', methods=['POST'])
def eval_code():
    if 'user_id' not in session or session['user_id'] not in allowed_users:
        return jsonify({"result": "Unauthorized"})

    code = request.json.get('code')
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {})
        result = stdout.getvalue()
    except Exception:
        result = traceback.format_exc()
    return jsonify({"result": result})
