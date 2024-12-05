#!/usr/bin/env python 

import rospy
from geometry_msgs.msg import Twist
import time
from math import floor

def ucgen():
     
    rospy.init_node('basla', anonymous=True) 
    
    topic_yayin = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
 
    cmd_hareket = Twist()
 
    uzunluk = 4   
    aci = 120   

    
    for _ in range(4):
        cmd_hareket.linear.x = uzunluk
        cmd_hareket.angular.z = 0
        topic_yayin.publish(cmd_hareket)
        rospy.loginfo("hareket --->")
        time.sleep(2)  

        # ddönüş 
        cmd_hareket.linear.x = 0
        cmd_hareket.angular.z = aci * (3.14 / 180)  
        topic_yayin.publish(cmd_hareket)
        rospy.loginfo("dönüş...")
        time.sleep(2) 

    # --------------  durdur ---------------
    cmd_hareket.linear.x = 0
    cmd_hareket.angular.z = 0
    topic_yayin.publish(cmd_hareket)
    rospy.loginfo("Görev tamamlandı.")

# fonsiyon çalıştırma 
ucgen() 
