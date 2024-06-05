import Adafruit_PCA9685
import json
import os

class ServoManager():

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.__servo_states = self.__load_states()
        self.__servo_limits = {
            0: {'angle': (0, 180), 'pwm': (130, 480)},
            1: {'angle': (65, 180), 'pwm': (270, 540)},
            2: {'angle': (0, 180), 'pwm': (160, 560)},
            3: {'angle': (0, 180), 'pwm': (200, 540)},
            4: {'angle': (0, 180), 'pwm': (120, 300)}
        }
        self.__servo_calibrations = {
            0: (130, 310, 480),
            1: (120, 330, 540),
            2: (160, 360, 560),
            3: (200, 330, 540),
            4: (120, 300, 300)
        }
        self.__initial_positions = {
            0: 310,
            1: 330,
            2: 300,
            3: 330,
            4: 300
        }

    def set_servo_angle(self, channel, angle):
        if not self.__validate_angle(channel, angle):
            raise ValueError(f"El ángulo {angle} está fuera de los límites permitidos para el canal {channel}.")
        if not self.__validate_kinematics(channel, angle):
            raise ValueError("El movimiento resultante puede causar colisión o exceder los límites seguros del brazo.")

        pwm_value = self.__angle_to_pwm(channel, angle)
        self.pwm.set_pwm(channel, 0, pwm_value)
        self.__update_state(channel, angle, pwm_value)

    def set_servo_pwm(self, channel, pwm):
        if not self.__validate_pwm(channel, pwm):
            raise ValueError(f"El PWM {pwm} está fuera de los límites permitidos para el canal {channel}.")
        self.pwm.set_pwm(channel, 0, pwm)
        angle = self.__pwm_to_angle(channel, pwm)
        self.__update_state(channel, angle, pwm)

    def get_servo_angle(self, channel):
        return self.__servo_states.get(str(channel), {}).get('angle', None)

    def get_servo_pwm(self, channel):
        return self.__servo_states.get(str(channel), {}).get('pwm', None)

    def set_initial_position(self):
        for channel, pwm in self.__initial_positions.items():
            self.pwm.set_pwm(channel, 0, pwm)
            angle = self.__pwm_to_angle(channel, pwm)
            self.__update_state(channel, angle, pwm)

    def __validate_angle(self, channel, angle):
        if channel in self.__servo_limits:
            min_angle, max_angle = self.__servo_limits[channel]['angle']
            return min_angle <= angle <= max_angle
        return True

    def __validate_pwm(self, channel, pwm_value):
        if channel in self.__servo_limits:
            min_pwm, max_pwm = self.__servo_limits[channel]['pwm']
            return min_pwm <= pwm_value <= max_pwm
        return True

    def __validate_kinematics(self, channel, angle):
        # TODO: Implementar validación cinemática
        return True

    def __load_states(self):
        if os.path.exists('servo_states.json'):
            with open('servo_states.json', 'r') as file:
                return json.load(file)
        return {str(i): {'angle': 0, 'pwm': list(self.__initial_positions.values())[i]} for i in range(len(self.__initial_positions))}

    def __save_states(self, states):
        with open('servo_states.json', 'w') as file:
            json.dump(states, file)

    def __update_state(self, channel, angle, pwm):
        self.__servo_states[str(channel)] = {'angle': angle, 'pwm': pwm}
        self.__save_states(self.__servo_states)

    def __angle_to_pwm(self, channel, angle):
        min_pulse, mid_pulse, max_pulse = self.__servo_calibrations[channel]
        if angle <= 90:
            return min_pulse + (mid_pulse - min_pulse) * angle // 90
        else:
            return mid_pulse + (max_pulse - mid_pulse) * (angle - 90) // 90

    def __pwm_to_angle(self, channel, pwm):
        min_pulse, mid_pulse, max_pulse = self.__servo_calibrations[channel]
        if pwm <= mid_pulse:
            return 90 * (pwm - min_pulse) // (mid_pulse - min_pulse)
        else:
            return 90 + 90 * (pwm - mid_pulse) // (max_pulse - mid_pulse)
