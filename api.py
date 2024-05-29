from flask import Flask, request, jsonify
from servo_manager import ServoManager

app = Flask(__name__)
servo_manager = ServoManager()

@app.route('/servo/<int:channel>/<int:angle>', methods=['POST'])
def move_servo(channel, angle):
    try:
        servo_manager.set_servo_angle(channel, angle)
        return jsonify({'status': 'success', 'channel': channel, 'angle': angle}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/servo/initialize', methods=['POST'])
def initialize_servo():
    try:
        servo_manager.set_initial_position()
        return jsonify({'status': 'success', 'message': 'Servos initialized to default position'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
