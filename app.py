from flask import Flask, request, render_template, jsonify
import io, contextlib, traceback
from flask_cors import CORS
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eval', methods=['POST'])
def eval_code():
    code = request.json.get('code')
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {})
        result = stdout.getvalue()
    except Exception:
        result = traceback.format_exc()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
