# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import webiopi
import datetime
import time
import os

# Retrieve GPIO lib
GPIO = webiopi.GPIO

# Start mjpg-stream from raspicam module
#os.system('LD_LIBRARY_PATH=/usr/local/lib/mjpg-streamer/ /usr/local/lib/mjpg-streamer/mjpg_streamer -i "input_raspicam.so -fps 15 -q 50 -x 320 -y 240" -o "output_http.so -p 8001 -w /usr/local/www" &')

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

# Left motor GPIOs
L1=5 # H-Bridge 1
L2=6 # H-Bridge 2
LS=13 # H-Bridge 1,2EN

# Right motor GPIOs
R1=16 # H-Bridge 3
R2=20 # H-Bridge 4
RS=21 # H-Bridge 3,4EN

# -------------------------------------------------- #
# Convenient PWM Function                            #
# -------------------------------------------------- #

# Set the speed of two motors
def set_speed(speed):
    GPIO.pulseRatio(LS, speed)
    GPIO.pulseRatio(RS, speed)

# -------------------------------------------------- #
# Left Motor Functions                               #
# -------------------------------------------------- #

def left_stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)

def left_forward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

def left_backward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

# -------------------------------------------------- #
# Right Motor Functions                              #
# -------------------------------------------------- #
def right_stop():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)

def right_forward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)

def right_backward():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)

# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #
@webiopi.macro
def Go_Forward():
    left_forward()
    right_forward()

@webiopi.macro
def Go_Reverse():
    left_backward()
    right_backward()

@webiopi.macro
def Turn_Left():
    left_backward()
    right_forward()

@webiopi.macro
def Turn_Right():
    left_forward()
    right_backward()

@webiopi.macro
def Stop_Bot():
    left_stop()
    right_stop()
	
# Functions for Pan and Tilt
@webiopi.macro
def Look_Left():
    cmd = 'echo 0=+10 > /dev/servoblaster'
    os.system(cmd)
	
@webiopi.macro
def Look_Right():
    cmd = 'echo 0=-10 > /dev/servoblaster'
    os.system(cmd)
	
@webiopi.macro
def Center_Cam():
    cmd = 'echo 0=155 > /dev/servoblaster'
	cmd = 'echo 1=120 > /dev/servoblaster'
    os.system(cmd)
	
@webiopi.macro
def Look_Up():
    cmd = 'echo 1=-10 > /dev/servoblaster'
    os.system(cmd)
	
@webiopi.macro
def Look_Down():
    cmd = 'echo 1=+10 > /dev/servoblaster'
    os.system(cmd)
	
# Functions for arm...still needs center and min max tweaking
@webiopi.macro
def Shoulder_Up():
	cmd = 'echo 3=+10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro
def Shoulder_Down():
	cmd = 'echo 3=-10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Shoulder_Left():
	cmd = 'echo 2=+10 > /dev/servoblaster'
	os.system(cmd)
	
@webiopi.macro	
def Shoulder_Right():
	cmd = 'echo 2=-10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Elbow_Extend():
	cmd = 'echo 4=+10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Elbow_Retract():
	cmd = 'echo 4=-10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Hand_Left():
	cmd = 'echo 5=+10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Hand_Right():
	cmd = 'echo 5=-10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Hand_Open():
	cmd = 'echo 6=+10 > /dev/servoblaster'
	os.system(cmd)

@webiopi.macro	
def Hand_Close():
	cmd = 'echo 6=-10 > /dev/servoblaster'
	os.system(cmd)
	

# Called by WebIOPi at script loading
def setup():
    # Setup GPIOs
    GPIO.setFunction(LS, GPIO.PWM)
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)
    
    GPIO.setFunction(RS, GPIO.PWM)
    GPIO.setFunction(R1, GPIO.OUT)
    GPIO.setFunction(R2, GPIO.OUT)

    set_speed(0.5)
    Stop_Bot()


# Called by WebIOPi at server shutdown
def destroy():

# Shutdown mjpg-stream from raspicam module, commented out since using diff streamer
    #os.system('kill $(pgrep mjpg_streamer) > /dev/null 2>&1')

    # Reset GPIO functions
    GPIO.setFunction(LS, GPIO.IN)
    GPIO.setFunction(L1, GPIO.IN)
    GPIO.setFunction(L2, GPIO.IN)
    
    GPIO.setFunction(RS, GPIO.IN)
    GPIO.setFunction(R1, GPIO.IN)
    GPIO.setFunction(R2, GPIO.IN)
    
