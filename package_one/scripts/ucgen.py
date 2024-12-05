#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# Minimum mesafe (metre) - engel algılama mesafesi
MIN_DISTANCE = 0.5  

def lidar_callback(scan_data):
    """
    LiDAR verilerini işler ve engel algılanırsa robotu durdurur.
    """
    # Tüm mesafeleri kontrol et
    ranges = scan_data.ranges
    
    # Engeli algıla (LiDAR verisinde 'inf' ya da çok küçük değerler olabilir)
    if any(distance < MIN_DISTANCE for distance in ranges if distance > 0):
        rospy.loginfo("Engel algılandı! Robot duruyor.")
        stop_robot()
    else:
        move_forward()

def stop_robot():
    """
    Robotu durdurmak için sıfır hız gönderir.
    """
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.0
    cmd_vel.angular.z = 0.0
    pub.publish(cmd_vel)

def move_forward():
    """
    Robotu ileri hareket ettirir.
    """
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.2  # İleri hız
    cmd_vel.angular.z = 0.0  # Düz bir çizgide hareket
    pub.publish(cmd_vel)

if __name__ == '__main__':
    try:
        # ROS düğümünü başlat
        rospy.init_node('obstacle_avoidance', anonymous=True)
        
        # Publisher (hareket komutları)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Subscriber (LiDAR verileri)
        rospy.Subscriber('/scan', LaserScan, lidar_callback)
        
        rospy.loginfo("Engel algılama ve durdurma başlatıldı.")
        
        # ROS döngüsünü çalıştır
        rospy.spin()
    
    except rospy.ROSInterruptException:
        pass
