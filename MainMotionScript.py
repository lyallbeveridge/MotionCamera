# A simple program designed to take a webcam picture when a PIR sensor is activated
# 9APR18
# By Lyall Beveridge

import onionGpio
import time
import os
import sys
import json


### FUNCTION DEFINITIONS ###

# An exit sequence that can be called on keyboard interrupt or other errors
def cleanExit():
	sensor._freeGpio()					# Cleanup sensor GPIO
	sys.exit()							# Exit cleanly


### SETUP ###

# -- Read in the JSON Settings
try:
	with open('settings.json', 'r') as settings_file:
		settings = json.load(settings_file)
	print str(settings['welcome_msg'])		# Print the welcome message to test JSON
	# Store the values in variables for readability
	n_snaps = settings['n_snaps']
	min_snap_interval = settings['min_snap_interval']
except IOError as e:
	print(e)								# Error printing should work for generic (not just IOError)
	print "Settings not found"
	cleanExit()
else:
	settings_file.close()					# Close and free up the system resources

# -- Set up the GPIO pins

# Set up the LED
ledPin = 19								# Set the pin
led = onionGpio.OnionGpio(ledPin)		# Instantiate the pin as a GPIO object
led.setOutputDirection()				# Set direction
print "LED should flash"
for light in range(0,3):				# Blink to test
	led.setValue(1)
	time.sleep(0.1)
	led.setValue(0)
	time.sleep(0.1)
print "LED testing complete"

# Set up the PIR Sensor
sensePin = 11							# Set the pin
sensor = onionGpio.OnionGpio(sensePin)	# Instantiate the pin as a GPIO object
sensor.setInputDirection()				# Set direction

lastSnap = time.time()					# Set up the timer
lastPir = 0								# Track changes in the pir system


### MAIN ###

try:
	print "Launching..."
	while 1:
		pir = sensor.getValue()			# Get the sensor value
		elapsed = time.time() - lastSnap# Get the time difference
		# If the sensor is high and the timer has elapsed past 30 seconds
		if (int(pir) == 1 and int(lastPir) == 0):
			print "Motion detected!"
			if (int(elapsed) >= min_snap_interval):
				# Take a snapshot
				print "Taking snapshot!"
				for snap in range(0, n_snaps):
					os.system('fswebcam -r 1280x720 /tmp/mounts/SD-P1/sd_snapshots/home_test1/"%Y-%m-%d_%H%M%S".jpg');
				lastSnap = time.time()		# Restart the timer
			
		led.setValue(pir)				# Light up the LED if the sensor is high
		# print "pir state: " + str(pir) + "lastPir state: " + str(lastPir) + "elapsed: " + str(elapsed) + "\n"
		lastPir = pir					# Update Pir value
		time.sleep(1)
	
except KeyboardInterrupt:				# If CTRL+C is pressed, exit cleanly:
	cleanExit()