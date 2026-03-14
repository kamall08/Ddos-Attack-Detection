import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from analyzer import analyze_log
from log_generator import generate_log

app = Flask(__name__)
# Generate a secret key if needed for sessions
app.secret_key = "super_secret_log_defender_key"

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit

ALLOWED_EXTENSIONS = {'txt', 'log'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Store latest analysis results in memory (simple approach for single-user/demo)
latest_results = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global latest_results
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            latest_results = analyze_log(content, threshold=100)
            
            return redirect(url_for('report'))
            
        except Exception as e:
            return render_template('index.html', error=f"Error analyzing file: {str(e)}")
            
    return render_template('index.html', error="Invalid file type. Please upload .txt or .log files.")

@app.route('/analyze-demo')
def analyze_demo():
    """Generates a demo log and analyzes it immediately"""
    global latest_results
    try:
        generate_log()
        # Read the generated log
        log_path = os.path.join(app.config['UPLOAD_FOLDER'], 'server.log')
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        latest_results = analyze_log(content, threshold=100)
        return redirect(url_for('report'))
    except Exception as e:
        return render_template('index.html', error=f"Error running demo: {str(e)}")

@app.route('/ip-analysis')
def ip_analysis():
    global latest_results
    if not latest_results:
        return redirect(url_for('index'))
    return render_template('ip_analysis.html', results=latest_results)

@app.route('/report')
def report():
    global latest_results
    if not latest_results:
        return redirect(url_for('index'))
    return render_template('report.html', results=latest_results)

@app.route('/threat-intel')
def threat_intel():
    global latest_results
    if not latest_results:
        return redirect(url_for('index'))
    # Extract only suspicious and malicious ips
    threat_ips = [ip for ip in latest_results.get('all_ips', []) if ip['status'] in ['Suspicious', 'Malicious']]
    return render_template('threat_intel.html', results=latest_results, threat_ips=threat_ips)

if __name__ == '__main__':
    print("Starting Log Defender Server...")
    app.run(debug=True, port=5000)
