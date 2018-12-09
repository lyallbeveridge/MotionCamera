# This program will allow the snapshot function from the fswebcam to be triggered by the sensor

import onionGpio
import time
import os
import sys

# set up the GPIO pins

# set up the LED
ledPin = 19							# Set the pin
led = onionGpio.OnionGpio(ledPin)	# Instantiate the pin as a GPIO object
led.setOutputDirection()			# Set direction

# set up the PIR Sensor
sensePin = 11						# Set the pin
sensor = onionGpio.OnionGpio(sensePin)	# Instantiate the pin as a GPIO object
# sensor._freeGpio()					# Free the sensor first
sensor.setInputDirection()			# Set direction

lastSnap = time.time()				# set up the timer
lastPir = 0;						# track the timer
pir = 0;							# test the comparison operator


try:
	while 1:
		pir = sensor.getValue()		# Get the sensor value
		
		
		elapsed = time.time() - lastSnap	# Get the time difference
		# If the sensor is high and the timer has elapsed past 30 seconds
		if (int(pir) == 1 and int(elapsed) >= 20):
			print "Taking snapshot!"
			
			# Take a snapshot
			os.system('fswebcam -r 1280x720 /tmp/mounts/SD-P1/sd_snapshots/home_test1/"%Y-%m-%d_%H%M%S".jpg');
			lastSnap = time.time()	# Restart the timer
			
		led.setValue(pir)			# Light up the LED if the sensor is high
		print "pir state: " + str(pir) + "lastPir state: " + str(lastPir) + "elapsed: " + str(elapsed) + "\n"
		
		lastPir = pir
		time.sleep(1)
	
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    # led._freeGpio()
    sensor._freeGpio()	# cleanup all GPIO