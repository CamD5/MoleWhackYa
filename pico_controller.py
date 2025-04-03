from machine import Pin, PWM
import time
import sys

# Hardware Setup
SERVO_PIN = 0  # GP0 (Pin 1)
IR_SENSOR_PIN = 1  # GP1 (Pin 2)

servo = PWM(Pin(SERVO_PIN))
servo.freq(50)  # Servos use 50Hz
ir_sensor = Pin(IR_SENSOR_PIN, Pin.IN, Pin.PULL_UP)

def set_servo_angle(angle):
    """Convert angle (0-180) to PWM duty cycle"""
    duty = 2500 + (angle * 7500 / 180)  # 2500-10000 range (~0°-180°)
    servo.duty_u16(int(duty))

def check_hammer_hit():
    return not ir_sensor.value()  # Returns True when beam is broken

# Main loop: Wait for commands from laptop
while True:
    command = sys.stdin.readline().strip()
    
    if command == "RAISE":
        set_servo_angle(90)  # Mole up
        print("ACK_RAISE")  # Acknowledge
        
    elif command == "LOWER":
        set_servo_angle(0)  # Mole down
        print("ACK_LOWER")
        
    elif command == "CHECK_HIT":
        print("HIT" if check_hammer_hit() else "MISS")