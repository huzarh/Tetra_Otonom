#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def don(): 
    cmd_vel = Twist()
    cmd_vel.linear.x = 0
    cmd_vel.angular.z = 1 # hızı burdan ayarlayabiriz
    pub.publish(cmd_vel)

 
rospy.init_node('nesne_algılama_icin_donus', anonymous=True)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

rate = rospy.Rate(10)  

while not rospy.is_shutdown():
    don()   
    rate.sleep()    
