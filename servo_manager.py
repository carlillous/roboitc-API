import Adafruit_PCA9685


class ServoManager:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        # Definir los límites y posiciones iniciales
        self.servo_limits = {
            0: {'min': 100, 'max': 560, 'initial': 80},  # Servo en canal 0
            3: {'min': 200, 'max': 500, 'initial': 90, 'limited': True},  # Servo en canal 3
            'default': {'min': 100, 'max': 560}
        }

    def set_servo_angle(self, channel, angle):
        # Obtener los límites para el servo especificado
        servo_min = self.servo_limits[channel]['min']
        servo_max = self.servo_limits[channel]['max']

        # Asegurar que el ángulo esté dentro de los límites permitidos
        if 'limited' in self.servo_limits[channel] and self.servo_limits[channel]['limited']:
            angle = max(min(angle, 175), 50)

        # Convertir el ángulo a un pulso
        pulse = servo_min + (angle * (servo_max - servo_min) // 180)
        self.pwm.set_pwm(channel, 0, pulse)

    def set_initial_position(self):
        # Establecer la posición inicial para cada servo
        for channel, settings in self.servo_limits.items():
            if isinstance(channel, int):  # Asegurarse de que el canal es un número
                initial_angle = settings.get('initial', 90)  # Por defecto 90 grados si no se especifica
                pulse = settings['min'] + (initial_angle * (settings['max'] - settings['min']) // 180)
                self.pwm.set_pwm(channel, 0, pulse)
