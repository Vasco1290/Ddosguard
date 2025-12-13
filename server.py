from flask import Flask, request
import time
import logging

app = Flask(__name__)

# Configure logging to a file
logging.basicConfig(filename='traffic.log', level=logging.INFO, format='%(asctime)s %(message)s')


@app.route('/')
def home():
    time.sleep(0.2)  # simulate processing delay
    ip = request.remote_addr
    logging.info(f"IP: {ip}")
    return "Server is running"


if __name__ == "__main__":
    app.run(port=5000)
