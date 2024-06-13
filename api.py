from flask import Flask, request, jsonify
from servo_manager import ServoManager
from system_status import SystemStatus
from motor_controller import MotorControl

app = Flask(__name__)
servo_manager = ServoManager()
motor_control = MotorControl()

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

@app.route('/servo/angles', methods=['GET'])
def get_angles():
    try:
        angles = []
        for i in range(0,5):
            angle = servo_manager.get_servo_angle(i)
            angles.append(angle)
        if angles is None:
            return jsonify({'status': 'error', 'message': 'Error'}), 404
        return jsonify({'status': 'success', 'angles':angles}), 200
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

@app.route('/motor/start', methods=['PUT'])
def start_motor():
    try:
        motor_control.setup()
        return jsonify({'status': 'success', 'message': 'Motor initialized and started'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
@app.route('/motor/move', methods=['PUT'])
def move_motor():
    try:
        data = request.json
        if data is None:
            raise ValueError("No JSON data provided")
        speed = data.get('speed', 100)
        direction = data.get('direction')
        turn = data.get('turn', 'no')
        motor_control.move(speed=speed, direction=direction, turn=turn)
        return jsonify({'status': 'success', 'message': f'Motor moving {direction}, {turn} at {speed}'}), 200
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/motor/stop', methods=['PUT'])
def stop_motor():
    try:
        motor_control.stop()
        return jsonify({'status': 'success', 'message': 'Motor stopped'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/motor/clear', methods=['PUT'])
def clear_motor():
    try:
        motor_control.reset()
        return jsonify({'status': 'success', 'message': 'Motor Instance cleared'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)