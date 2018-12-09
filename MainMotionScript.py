# A simple program designed to take a webcam picture when a PIR sensor is activated
# 9APR18
# By Lyall Beveridge

import onionGpio
import time
import os
import sys

# -- Set up the GPIO pins

# Set up the LED
ledPin = 19								# Set the pin
led = onionGpio.OnionGpio(ledPin)		# Instantiate the pin as a GPIO object
led.setOutputDirection()				# Set direction

# Set up the PIR Sensor
sensePin = 11							# Set the pin
sensor = onionGpio.OnionGpio(sensePin)	# Instantiate the pin as a GPIO object
sensor.setInputDirection()				# Set direction

lastSnap = time.time()					# Set up the timer

try:
	while 1:
		pir = sensor.getValue()			# Get the sensor value
		elapsed = time.time() - lastSnap	# Get the time difference
		# If the sensor is high and the timer has elapsed past 30 seconds
		if (int(pir) == 1 and int(elapsed) >= 20):
			# Take a snapshot
			print "Taking snapshot!"
			os.system('fswebcam -r 1280x720 /tmp/mounts/SD-P1/sd_snapshots/home_test1/"%Y-%m-%d_%H%M%S".jpg');
			lastSnap = time.time()		# Restart the timer
			
		led.setValue(pir)				# Light up the LED if the sensor is high
		# print "pir state: " + str(pir) + "lastPir state: " + str(lastPir) + "elapsed: " + str(elapsed) + "\n"
		time.sleep(1)
	
except KeyboardInterrupt:				# If CTRL+C is pressed, exit cleanly:
    sensor._freeGpio()					# Cleanup sensor GPIO
    sys.exit()							# Exit cleanly
	