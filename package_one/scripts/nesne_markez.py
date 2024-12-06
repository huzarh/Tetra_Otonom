#!/usr/bin/env python3
# -- coding: utf-8 --

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO

class Kamera():
    def __init__(self):
        rospy.init_node("kamera_dugumu")
        self.bridge = CvBridge()
        
        # yolo modeli github:https://github.com/ultralytics/ultralytics?tab=readme-ov-file
        self.model = YOLO("package_one/models/yolov8l.pt")
        
        # wafflipiden gelen görüntü
        rospy.Subscriber("camera/rgb/image_raw", Image, self.kameraCallback)
        rospy.spin()
        
    def kameraCallback(self, mesaj):
        cv_resim = self.bridge.imgmsg_to_cv2(mesaj, "bgr8")
        
        # yolo filterle
        cikis = self.model(cv_resim)

        # ui
        for result in cikis:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Nesneyi belirleme
                cv2.rectangle(cv_resim, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # nesne adı
                cv2.putText(cv_resim, result.names[int(box.cls[0])], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        gri = cv2.cvtColor(cv_resim, cv2.COLOR_BGR2GRAY)
        
        # gri renkiden kenarı algılama opencv
        kenar = cv2.Canny(gri, 50, 150)
        
        x , _ = cv2.findContours(kenar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for arg in x:
            # -------- filtrele ---------
            if cv2.contourArea(arg) > 100:
                # merkez
                M = cv2.moments(arg)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) 
                    cy = int(M["m01"] / M["m00"])  
                    
                   
                    cv2.circle(cv_resim, (cx, cy), 5, (0, 0, 75), -1)  # açık kırmızı renkle merkez noktası
                    cv2.putText(cv_resim, "merkez", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                
                # yolonun haricinde obj sayılabilir nesneleri belirleme 
                x, y, w, h = cv2.boundingRect(arg)
                cv2.rectangle(cv_resim, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # çıkış sayfa
        cv2.imshow("----- Kamera -----------", cv_resim) 
        cv2.waitKey(1)

Kamera()# <-------------------------- fonksyon çalıştırma -----<<<<<<<<<<<<<<<
