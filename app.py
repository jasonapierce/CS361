from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)
start_time = None
stop_time = None

@app.route('/current-time', methods=['GET'])
def get_current_time():
    timezone = request.args.get('timezone', 'UTC')
    fmt = request.args.get('format', 'iso8601')

    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        return jsonify({"error": "Unknown timezone"}), 400

    now = datetime.now(tz)

    if fmt == 'timestamp':
        time_str = int(now.timestamp())  # seconds since epoch
    else:
        time_str = now.isoformat()

    return jsonify({"utc_time": time_str})

@app.route('/start-timer', methods=['GET'])
def start_timer():
    global start_time
    timezone = request.args.get('timezone', 'UTC')
    fmt = request.args.get('format', 'iso8601')

    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        return jsonify({"error": "Unknown timezone"}), 400

    start_time = datetime.now(tz)

    if fmt == 'timestamp':
        time_str = int(start_time.timestamp())  # seconds since epoch
    else:
        time_str = start_time.isoformat()

    return jsonify({"start_time": time_str})

@app.route('/stop-timer', methods=['GET'])
def stop_timer():
    global start_time
    global stop_time
    timezone = request.args.get('timezone', 'UTC')
    fmt = request.args.get('format', 'iso8601')

    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        return jsonify({"error": "Unknown timezone"}), 400

    stop_time = datetime.now(tz)

    if fmt == 'timestamp':
        time_str = int(stop_time.timestamp())  # seconds since epoch
    else:
        time_str = stop_time.isoformat()

    if start_time is None:
        return jsonify({"elapsed_time": "timer not started"})
    else:
        elapsed_time = stop_time - start_time
        start_time = None
        return jsonify({"elapsed_time": str(elapsed_time)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
