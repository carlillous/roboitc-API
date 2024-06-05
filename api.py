from flask import Flask, request, jsonify
from servo_manager import ServoManager
from system_status import SystemStatus

app = Flask(__name__)
servo_manager = ServoManager()

@app.route('/servo/<int:channel>/angle', methods=['GET'])
def get_servo_angle(channel):
    try:
        angle = servo_manager.get_servo_angle(channel)
        if angle is None:
            return jsonify({'status': 'error', 'message': 'Channel not found'}), 404
        return jsonify({'status': 'success', 'channel': channel, 'angle': angle}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/servo/<int:channel>/angle/<int:angle>', methods=['PUT'])
def move_servo_angle(channel, angle):
    try:
        servo_manager.set_servo_angle(channel,angle)
        return jsonify({'status': 'success', 'channel': channel, 'angle': angle}), 200
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/servo/<int:channel>/pwm/<int:pwm>', methods=['PUT'])
def move_servo_pwm(channel, pwm):
    try:
        servo_manager.set_servo_pwm(channel,pwm)
        return jsonify({'status': 'success', 'channel': channel, 'pwm': pwm}), 200
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/servo/<int:channel>/pwm', methods=['GET'])
def get_servo_pwm(channel):
    try:
        pwm = servo_manager.get_servo_pwm(channel)
        if pwm is None:
            return jsonify({'status': 'error', 'message': 'Channel not found'}), 404
        return jsonify({'status': 'success', 'channel': channel, 'pwm': pwm}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/servo/initialize', methods=['PUT'])
def initialize_servo():
    try:
        servo_manager.set_initial_position()
        return jsonify({'status': 'success', 'message': 'Servos initialized to default position'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_system_status():
    try:
        cpu_temp = SystemStatus.get_cpu_temperature()
        cpu_usage = SystemStatus.get_cpu_usage()
        ram_usage = SystemStatus.get_ram_usage()

        status = f"CPU Temperature: {cpu_temp} °C, CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%"
        return jsonify({'status': 'success', 'message': status}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)