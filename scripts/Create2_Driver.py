#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import struct

try:
    import serial
except ImportError:
    tkMessageBox.showerror('Import error', 'Please install pyserial.')
    raise

def sendCommandASCII(command):
    cmd = ""
    for v in command.split():
        cmd += chr(int(v))
    sendCommandRaw(cmd)

# Implement:
#	

# sendCommandRaw takes a string interpreted as a byte array
def sendCommandRaw(command):
    global connection
    try:
        if connection is not None:
            connection.write(command)
        else:
            tkMessageBox.showerror('Not connected!', 'Not connected to a robot!')
            print "Not connected."
    except serial.SerialException:
        print "Lost connection"
        tkMessageBox.showinfo('Uh-oh', "Lost connection to the robot!")
        connection = None

def callback(Velocity):
    forward = Velocity.linear.x
    yaw = Velocity.angular.z
    vr = yaw*(.4/2)+forward
    vl = -yaw*(.4/2)+forward
    speed = 550
    cmd = struct.pack(">Bhh", 145, speed*vr, speed*vl)
    sendCommandRaw(cmd)
    
def listener():

    rospy.init_node('Create_Driver', anonymous=True)
    rospy.Subscriber("Create2_Driver/cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    global connection
    connection = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
    sendCommandASCII('128')
    sendCommandASCII('132')
    listener()
