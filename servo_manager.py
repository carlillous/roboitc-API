import Adafruit_PCA9685
import json
import os


class ServoManager():

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.__servo_states = self.__load_states()
        self.__servo_limits = {
            0: (0, 180),
            1: (0, 180),
            2: (0, 180),
            3: (50, 175),
            4: (0, 180)
        }

    def set_servo_angle(self, channel, angle):
        if not self.__validate_angle(channel, angle):
            raise ValueError(f"El ángulo {angle} está fuera de los límites permitidos para el canal {channel}.")
        if not self.__validate_kinematics(channel, angle):
            raise ValueError("El movimiento resultante puede causar colisión o exceder los límites seguros del brazo.")

        # Convertir el ángulo (0-180) a un pulso (servo_min-servo_max)
        servo_min = 100  # Pulso mínimo (0 grados)
        servo_max = 560  # Pulso máximo (180 grados)
        pulse = servo_min + (angle * (servo_max - servo_min) // 180)
        self.pwm.set_pwm(channel, 0, pulse)
        self.__update_state(channel, angle)

    def get_servo_angle(self, channel):
        return self.__servo_states.get(str(channel), None)

    def set_initial_position(self):
        self.pwm.set_all_pwm(0, 330)
        for i in range(len(self.__servo_states)):
            self.__update_state(i, 90)

    def __validate_angle(self, channel, angle):
        if channel in self.__servo_limits:
            min_angle, max_angle = self.__servo_limits[channel]
            return min_angle <= angle <= max_angle
        return True

    def __validate_kinematics(self, channel, angle):
        #TODO
        return True

    def __load_states(self):
        if os.path.exists('servo_states.json'):
            with open('servo_states.json', 'r') as file:
                return json.load(file)
        return {str(i): 0 for i in range(5)}

    def __save_states(self, states):
        with open('servo_states.json', 'w') as file:
            json.dump(states, file)

    def __update_state(self, channel, angle):
        self.__servo_states[str(channel)] = angle
        self.__save_states(self.__servo_states)
