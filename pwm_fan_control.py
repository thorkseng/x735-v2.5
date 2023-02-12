#!/usr/bin/python
import pigpio
import time
import sys

servo = 13

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 25000 )
pwm.set_PWM_range(servo, 100)

# array of lists [(Max_CPU_Temp, Fan speed), ...]
temp_duty_pairs = [(30, 40), (50, 50), (55, 75), (60, 90), (65, 100), (-float('inf'), 0)]

while True:
     try:
          try:
               with open("/sys/class/thermal/thermal_zone0/temp") as file:
                    temp = float(file.read()) / 1000.00
                    temp = float('%.2f' % temp)
          except:
               print("Failed to read temperature, retrying in 1 second...")
               time.sleep(1)
               continue

          for temp_threshold, duty in temp_duty_pairs:
               if temp > temp_threshold:
                    pwm.set_PWM_dutycycle(servo, duty)
                    break
          time.sleep(1)

     except KeyboardInterrupt:
          print("Exiting Servo Temperature Control Service...")
          sys.exit(0)
