import Adafruit_PCA9685

class ServoManager():

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

    def set_servo_angle(self,channel, angle):
        if channel == 3 and (50>angle or angle>175):
            raise ValueError("El ángulo debe estar entre 50 y 175 grados para el canal 3.")
        # Convertir el ángulo (0-180) a un pulso (servo_min-servo_max)
        servo_min = 100  # Pulso mínimo (0 grados)
        servo_max = 560  # Pulso máximo (180 grados)
        pulse = servo_min + (angle * (servo_max - servo_min) // 180)
        self.pwm.set_pwm(channel, 0, pulse)

    def set_initial_position(self):
        self.pwm.set_all_pwm(0, 330)