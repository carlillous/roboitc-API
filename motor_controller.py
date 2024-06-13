import RPi.GPIO as GPIO


class MotorControl:
    """ motor_EN_A: Pin7  |  motor_EN_B: Pin11
     motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12"""
    Motor_A_EN, Motor_B_EN = 4, 17
    Motor_A_Pin1, Motor_A_Pin2 = 26, 21
    Motor_B_Pin1, Motor_B_Pin2 = 27, 18

    Dir_forward, Dir_backward = 0, 1

    def __init__(self):
        self.pwm_A = None
        self.pwm_B = None
        self.setup()

    def stop(self):
        GPIO.output(MotorControl.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(MotorControl.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(MotorControl.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(MotorControl.Motor_B_Pin2, GPIO.LOW)
        GPIO.output(MotorControl.Motor_A_EN, GPIO.LOW)
        GPIO.output(MotorControl.Motor_B_EN, GPIO.LOW)

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MotorControl.Motor_A_EN, GPIO.OUT)
        GPIO.setup(MotorControl.Motor_B_EN, GPIO.OUT)
        GPIO.setup(MotorControl.Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(MotorControl.Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(MotorControl.Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(MotorControl.Motor_B_Pin2, GPIO.OUT)

        self.stop()
        self.pwm_A = GPIO.PWM(MotorControl.Motor_A_EN, 1000)
        self.pwm_B = GPIO.PWM(MotorControl.Motor_B_EN, 1000)
        self.pwm_A.start(0)
        self.pwm_B.start(0)

    def __control_motor(self, pin1, pin2, en, pwm, status, direction, speed):
        if status == 0:  # stop
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)
            GPIO.output(en, GPIO.LOW)
        else:
            if direction == MotorControl.Dir_forward:
                GPIO.output(pin1, GPIO.HIGH)
                GPIO.output(pin2, GPIO.LOW)
                pwm.start(100)
                pwm.ChangeDutyCycle(speed)
            elif direction == MotorControl.Dir_backward:
                GPIO.output(pin1, GPIO.LOW)
                GPIO.output(pin2, GPIO.HIGH)
                pwm.start(0)
                pwm.ChangeDutyCycle(speed)

    def __motor_left(self, status, direction, speed):
        self.__control_motor(MotorControl.Motor_B_Pin1, MotorControl.Motor_B_Pin2, MotorControl.Motor_B_EN, self.pwm_B,
                             status, direction, speed)

    def __motor_right(self, status, direction, speed):
        self.__control_motor(MotorControl.Motor_A_Pin1, MotorControl.Motor_A_Pin2, MotorControl.Motor_A_EN, self.pwm_A,
                             status, direction, speed)

    def move(self, speed=100, direction=None, turn=None):  # 0 < radius <= 1
        if direction == 'forward':
            if turn == 'right':
                self.__motor_left(0, MotorControl.Dir_forward, speed)
                self.__motor_right(1, MotorControl.Dir_forward, speed)
            elif turn == 'left':
                self.__motor_left(1, MotorControl.Dir_forward, speed)
                self.__motor_right(0, MotorControl.Dir_forward, speed)
            else:
                self.__motor_left(1, MotorControl.Dir_forward, speed)
                self.__motor_right(1, MotorControl.Dir_forward, speed)
        elif direction == 'backward':
            if turn == 'right':
                self.__motor_left(0, MotorControl.Dir_backward, speed)
                self.__motor_right(1, MotorControl.Dir_backward, speed)
            elif turn == 'left':
                self.__motor_left(1, MotorControl.Dir_backward, speed)
                self.__motor_right(0, MotorControl.Dir_backward, speed)
            else:
                self.__motor_left(1, MotorControl.Dir_backward, speed)
                self.__motor_right(1, MotorControl.Dir_backward, speed)
        elif direction is None:
            if turn == 'right':
                self.__motor_left(1, MotorControl.Dir_backward, speed)
                self.__motor_right(1, MotorControl.Dir_forward, speed)
            elif turn == 'left':
                self.__motor_left(1, MotorControl.Dir_forward, speed)
                self.__motor_right(1, MotorControl.Dir_backward, speed)
            else:
                self.stop()
        else:
            pass

    def reset(self):
        self.stop()
        GPIO.cleanup()