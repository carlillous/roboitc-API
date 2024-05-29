import Adafruit_PCA9685
import json
import os

class ServoManager():

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.__servo_states = self.__load_states()

    def set_servo_angle(self,channel, angle):
        if channel == 3 and (50>angle or angle>175):
            raise ValueError("El ángulo debe estar entre 50 y 175 grados para el canal 3.")
        # Convertir el ángulo (0-180) a un pulso (servo_min-servo_max)
        servo_min = 100  # Pulso mínimo (0 grados)
        servo_max = 560  # Pulso máximo (180 grados)
        pulse = servo_min + (angle * (servo_max - servo_min) // 180)
        self.pwm.set_pwm(channel, 0, pulse)
        self.__update_state(channel,angle)

    def get_servo_angle(self,channel):
        return self.__servo_states.get(str(channel), None)

    def set_initial_position(self):
        self.pwm.set_all_pwm(0, 330)
        for i in range(len(self.__servo_states)):
            self.__update_state(i, 0)

    def __load_states(self):
        if os.path.exists('servo_states.json'):
            with open('servo_states.json', 'r') as file:
                return json.load(file)
        return {str(i): 0 for i in range(5)}

    def __save_states(self,states):
        with open('servo_states.json', 'w') as file:
            json.dump(states, file)

    def __update_state(self,channel, angle):
        self.servo_states[str(channel)] = angle
        self.__save_states(self.servo_states)