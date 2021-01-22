#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from geometry_msgs.msg  import Twist, PoseStamped
from sensor_msgs.msg import Image, Range	
from rospy.numpy_msg import numpy_msg
from std_srvs.srv import *
from math import pow,atan2,sqrt
import sys
import time
PI = 3.1415926535897
takeOff = False
landed = False
returning = False	
destX = 0.0
destY = 0.0


def sendVelocityMessage(lx, ly, lz, ax, ay, az) :

	pub = rospy.Publisher('/cmd_vel',Twist, queue_size = 10)
	vel_msg = Twist()

	vel_msg.linear.x = lx
	vel_msg.linear.y = ly
	vel_msg.linear.z = lz
	vel_msg.angular.x = ax
	vel_msg.angular.y = ay
	vel_msg.angular.z = az

	pub.publish(vel_msg)	
		
def rangeCallback(rng) :

	global landed
	
	if  rng.range < 0.25 :
		landed = True
	else :
		landed = False	


def poseCallback(ps) :

	rate = rospy.Rate(300)
	poseX = ps.pose.position.x
	poseY = ps.pose.position.y
	poseZ = ps.pose.position.z
	
	#print "position x :", poseX
	#print "position y :", poseY
	#print "position z :", poseZ

	linX = 0
	linY = 0
	linZ = 0
	global takeOff, destX, destY, landed, returning



	if takeOff == False :

		if poseZ < 15.0 :
			sendVelocityMessage(0, 0, 5.0 ,0 ,0 ,0)	
		else :	
			takeOff = True

	if takeOff == True :
		
		distance = sqrt((poseX - destX)**2 + (poseY - destY)**2)
		print poseX, poseY, destX, destY, distance

		if  distance <= 2.0 and distance > 0.5 :
			
			if poseX < destX :
				linX = 0.1
			if poseX > destX :
				linX = -0.1
			if poseY < destY :
				linY = 0.1
			if poseY > destY :
				linY = -0.1

		elif distance <= 0.5 and distance > 0.09 :

			if poseX < destX :
				linX = 0.03
			if poseX > destX :
				linX = -0.03
			if poseY < destY :
				linY = 0.03
			if poseY > destY :
				linY = -0.03

		elif distance <= 0.09 :
			
			if landed == False :
				linZ = -0.4	
			else :	
				if returning == True :
					print "Baslangic noktasina donuldu, kapatiliyor..."
					rospy.signal_shutdown("Kapatiliyor...")
			
				print "Urun teslim edildi!"				
				#time.sleep(10) # 10 saniye bekle				
				destX = 0.0
				destY = 0.0
				returning = True
				takeOff = False		
				distance = 0			
				
		else :	

			if poseX < destX :
				linX = 3.0
			if poseX > destX :
				linX = -3.0
			if poseY < destY :
				linY = 3.0
			if poseY > destY :
				linY = -3.0
			
		sendVelocityMessage(linX, linY, linZ, 0, 0, 0)
		
	cv2.waitKey(3)	
	rate.sleep()
	
def imageCallback(data):

	frame = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
	rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	cv2.imshow("Camera",rgb_img)	
	
	
 
if __name__ == '__main__':

	while(True) :		 
		houseName = raw_input("Hedef ev : ") 
		if houseName == "" :
			print "Gecerli bir isim girin!"
		else :
			break
		
	with open("./.ros/locations.txt", "r") as file:
		houseFound = False
		for line in file :

			lineList = [x.strip() for x in line.split(',')]	

			if lineList[0] == houseName :		

				houseX = float(lineList[1])
				houseY = float(lineList[2])	
				houseFound = True
			
			if houseFound == True and lineList[0].startswith("station") == True :
				
				stationX = float(lineList[1])
				stationY = float(lineList[2])
				if destX == 0.0 and destY == 0.0 :
					destX = stationX
					destY = stationY
				else :
					currDist = sqrt((destX - houseX)**2 + (destY - houseY)**2 ) 
					newDist = sqrt((stationX - houseX)**2 + (stationY - houseY)**2 )
					if newDist < currDist :
						destX = stationX
						destY = stationY
		
		if houseFound == False :
			print "Kayitli ev bulunamadi!"	
			sys.exit()	
							
		print "Hedef konum : ", destX, " ", destY
		print "Kalkisa geciliyor!"

	try:
		rospy.init_node('hector_control', anonymous=True)				
		rospy.Subscriber("/front_cam/camera/image", numpy_msg(Image), imageCallback)
		rospy.Subscriber('/ground_truth_to_tf/pose', PoseStamped, poseCallback)
    		rospy.Subscriber('/sonar_height', Range, rangeCallback)
		rospy.spin()	
		
				
	except rospy.ROSInterruptException: 
		cv2.destroyAllWindows()
		pass
