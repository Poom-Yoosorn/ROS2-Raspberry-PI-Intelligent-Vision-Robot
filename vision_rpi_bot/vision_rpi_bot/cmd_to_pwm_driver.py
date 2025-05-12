import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
import time

class Velocity_subscriber(Node):

    def __init__(self):
        super().__init__('cmd_vel_subscriber')
        self.subscription = self.create_subscription(Twist,'/cmd_vel',self.cmd_to_pwm_callback,10)
        
        self.right_motor_a = 14
        self.right_motor_b = 15
        right_motor_en = 18

        self.left_motor_a = 5
        self.left_motor_b = 6
        left_motor_en = 13

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.right_motor_a, GPIO.OUT)
        GPIO.setup(self.right_motor_b, GPIO.OUT)
        GPIO.setup(right_motor_en, GPIO.OUT)

        GPIO.setup(self.left_motor_a, GPIO.OUT)
        GPIO.setup(self.left_motor_b, GPIO.OUT)
        GPIO.setup(left_motor_en, GPIO.OUT)

        self.pwm_r = GPIO.PWM(right_motor_en, 1000)
        self.pwm_l = GPIO.PWM(left_motor_en, 1000)

        self.pwm_r.start(75)
        self.pwm_l.start(75)    




    def cmd_to_pwm_callback(self, msg):
        right_wheel_vel = (msg.linear.x + msg.angular.z)/2
        left_wheel_vel = (msg.linear.x - msg.angular.z)/2

        print("right_wheel_vel",right_wheel_vel, "/", "left_wheel_vel",left_wheel_vel)

        GPIO.output(self.right_motor_a,right_wheel_vel > 0)
        GPIO.output(self.right_motor_b,right_wheel_vel < 0)

        GPIO.output(self.left_motor_a,left_wheel_vel > 0)
        GPIO.output(self.left_motor_b,left_wheel_vel < 0)


def main(args=None):
    rclpy.init(args=args)

    velocity_subscriber = Velocity_subscriber()

    try:
        rclpy.spin(velocity_subscriber)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        velocity_subscriber.destroy_node()
        GPIO.cleanup()  # <--- ADD THIS LINE HERE
        rclpy.shutdown()


if __name__ == '__main__':
    main()