# ddosguard.py

import random
import time
import threading
from flask import Flask, jsonify, render_template_string
from collections import defaultdict

# Flask App
app = Flask(__name__)

# Simulated traffic data
ip_request_count = defaultdict(int)
flagged_ips = set()
MAX_REQUESTS_PER_SECOND = 100
TRAFFIC_DURATION = 30  # seconds to run the traffic simulation

# HTML template for dashboard
DASHBOARD_HTML = """
<!doctype html>
<html>
<head>
    <title>DDoS Detection Dashboard</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <h1>DDoS Detection Dashboard</h1>
    <h3>Flagged IPs:</h3>
    <table>
        <tr><th>IP Address</th><th>Request Count</th></tr>
        {% for ip, count in data %}
        <tr><td>{{ ip }}</td><td>{{ count }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Generate random IP
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Traffic simulation
def simulate_traffic():
    start_time = time.time()
    while time.time() - start_time < TRAFFIC_DURATION:
        ip = generate_random_ip()
        requests = random.randint(1, 200)  # Random burst
        ip_request_count[ip] += requests

        if ip_request_count[ip] > MAX_REQUESTS_PER_SECOND:
            if ip not in flagged_ips:
                flagged_ips.add(ip)
                print(f"[ALERT] Potential DDoS detected from IP: {ip} ({ip_request_count[ip]} requests)")

        time.sleep(0.1)

# Flask route
@app.route("/")
def dashboard():
    data = [(ip, count) for ip, count in ip_request_count.items() if ip in flagged_ips]
    return render_template_string(DASHBOARD_HTML, data=data)

# CLI Monitor (in parallel)
def cli_monitor():
    while True:
        print(f"Total IPs tracked: {len(ip_request_count)} | Flagged: {len(flagged_ips)}")
        time.sleep(5)

# Start everything
if __name__ == "__main__":
    print("Starting DDoSGuard simulation...")

    # Thread 1: Traffic simulation
    t1 = threading.Thread(target=simulate_traffic)
    t1.start()

    # Thread 2: CLI Monitor
    t2 = threading.Thread(target=cli_monitor, daemon=True)
    t2.start()

    # Thread 3: Flask web server
    app.run(port=5000, debug=False)
