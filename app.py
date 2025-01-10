from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# Track the running process
global traffic_process
traffic_process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_traffic', methods=['POST'])
def start_traffic():
    global traffic_process
    
    # Get the IP and traffic speed
    target_ip = request.json.get('ip')
    traffic_speed = request.json.get('speed')

    if not target_ip or not traffic_speed:
        return jsonify({"error": "IP and speed are required"}), 400

    # Command to simulate traffic (example with 'iperf')
    command = [
        'iperf3', '-c', target_ip, '--bitrate', traffic_speed
    ]

    try:
        # Start the process
        traffic_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({"message": "Traffic generation started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop_traffic', methods=['POST'])
def stop_traffic():
    global traffic_process

    if traffic_process:
        traffic_process.terminate()
        traffic_process = None
        return jsonify({"message": "Traffic generation stopped"})

    return jsonify({"error": "No traffic generation process running"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)