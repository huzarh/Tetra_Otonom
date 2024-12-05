#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# engele çarpımadan durma mesafesi
durma = 0.5  
mevcut_hiz = 0.0

def lidar_veri(scan_data): 
    global mevcut_hiz
    # lidardan gelen mesafeler
    ranges = scan_data.ranges
    
    # çok küçük yada engel vb filtreleme
    if any(distance < durma for distance in ranges if distance > 0):
        rospy.loginfo(f"Engel var! robot hız: {mevcut_hiz},mesafe: {durma}")
        dur()
    else:
        ileri()

def dur():
    global mevcut_hiz
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.0
    cmd_vel.angular.z = 0.0
    mevcut_hiz = cmd_vel.linear.x  
    pub.publish(cmd_vel)

def ileri(): 
    global mevcut_hiz
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.5  
    cmd_vel.angular.z = 0  # düz = 0
    mevcut_hiz = cmd_vel.linear.x  
    pub.publish(cmd_vel) 


try:
    # düğüm
    rospy.init_node('mesafe_engel', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # LiDAR verileri sub--->
    rospy.Subscriber('/scan', LaserScan, lidar_veri)
    
    rospy.loginfo("Başlatıldı:")
    rospy.spin()

except rospy.ROSInterruptException:
    pass
