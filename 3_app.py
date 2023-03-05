# Set-ExecutionPolicy Unrestricted -Scope Process
# env\Scripts\activate

from flask import Flask, jsonify, request
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Endpoint to get the latest information for a device ID
@app.route('/device/<string:device_id>/latest', methods=['GET'])
def get_latest(device_id):
    data = r.hgetall(device_id)
    if data:
        latest_data = max(data.items(), key=lambda x: x[1]['time_stamp'])[1]
        return jsonify(latest_data)
    else:
        return jsonify({'error': 'Device ID not found.'})

# Endpoint to get the start and end locations for a device ID
@app.route('/device/<string:device_id>/locations', methods=['GET'])
def get_locations(device_id):
    data = r.hgetall(device_id)
    if data:
        locations = [{'latitude': d['latitude'], 'longitude': d['longitude']} for d in data.values()]
        start_location = locations[0]
        end_location = locations[-1]
        return jsonify({'location': f"{(start_location,end_location)}"})
    else:
        return jsonify({'error': 'Device ID not found.'})

# Endpoint to get all location points for a device ID within a specified time range
@app.route('/device/<string:device_id>/locationpoints', methods=['GET'])
def get_location_points(device_id):
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    data = r.hgetall(device_id)
    if data:
        location_points = [{'latitude': d['latitude'], 'longitude': d['longitude'], 'time_stamp': d['time_stamp']} for d in data.values() if start_time <= d['time_stamp'] <= end_time]
        return jsonify(location_points)
    else:
        return jsonify({'error': 'Device ID not found.'})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
