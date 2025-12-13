import time
import threading
from flask import Flask, jsonify, render_template_string
from collections import defaultdict

app = Flask(__name__)
log_file_path = 'traffic.log'

ip_request_count = defaultdict(int)
flagged_ips = set()
MAX_REQUESTS_PER_MINUTE = 100  # adjustable

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


def monitor_log():
    print("[+] Monitoring traffic.log for IP activity...")
    with open(log_file_path, "r") as f:
        f.seek(0, 2)  # Move to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            if "IP:" in line:
                ip = line.strip().split("IP:")[1].strip()
                ip_request_count[ip] += 1
                if ip_request_count[ip] > MAX_REQUESTS_PER_MINUTE:
                    if ip not in flagged_ips:
                        flagged_ips.add(ip)
                        print(f"[ALERT] Potential DDoS from {ip} ({ip_request_count[ip]} requests)")


@app.route("/")
def dashboard():
    data = [(ip, count) for ip, count in ip_request_count.items() if ip in flagged_ips]
    return render_template_string(DASHBOARD_HTML, data=data)


def cli_monitor():
    while True:
        print(f"Tracking {len(ip_request_count)} IPs | Flagged: {len(flagged_ips)}")
        time.sleep(5)


if __name__ == "__main__":
    print("Starting Real-Time DDoS Monitor...")
    t1 = threading.Thread(target=monitor_log)
    t1.start()
    t2 = threading.Thread(target=cli_monitor, daemon=True)
    t2.start()
    app.run(port=8000, debug=False)
