import sys
import time
import numpy as np
import tensorflow as tf
import cv2
import time
from FROZEN_GRAPH_HEAD import TensoflowHeadDector
from parinya import LINE


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT_HEAD = 'models/HEAD_DETECTION_300x300_ssd_mobilenetv2.pb'
line =LINE('6NKd0tSpKCnpyOXxidyHRmbWAJmiuScGyOQEPhnOQ5X')

#source = 'test_video/123.png'
source = 0

if __name__ == "__main__":
    tDetector = TensoflowHeadDector(PATH_TO_CKPT_HEAD)
    cap = cv2.VideoCapture(source)
      
    while True:
        t_start = time.time()
        ret, image = cap.read()
        #image = cv2.resize(imageza,(960, 540))
        if ret == 0:
            break
        im_height, im_width, im_channel = image.shape
        image = cv2.flip(image, 1)
        boxes, scores, classes, num_detections = tDetector.run(image)
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)

        localtime = time.asctime( time.localtime(time.time()) )
       
        counter = 0
        x = 0 
    
        for score, box in zip(scores, boxes):
            if score > 0.7:

                left = int(box[1]*im_width)
                top = int(box[0]*im_height)
                right = int(box[3]*im_width)
                bottom = int(box[2]*im_height)
                box_width = right-left
                box_height = bottom-top
               
                x += 1
                counter += 1
                
                cv2.putText(image, 'Head: {:.2f}%'.format(score*100), (left, top-5), 0, 5e-3 * 130, (255,0,0),2) 
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), int(round(im_height/150)), 8)
           
            elif 0 < counter < 2:  
                cv2.putText(image,'Humans Detected :'+str(counter),(10, 50), 0, 5e-3 * 130, (0,0,0), 2)
                cv2.putText(image,localtime,(10, 73), 0, 5e-3 * 130, (0,0,0), 2)  

            elif counter == 0:                               
                cv2.putText(image,'No People Detected',(10, 50), 0, 5e-3 * 130, (0,0,0), 2)
                cv2.putText(image,localtime,(10, 73), 0, 5e-3 * 130, (0,0,0), 2)  
                x = 0 
                                                                
            elif counter >= 2:
                cv2.putText(image,'Too many people !!!!! ',(10, 93), 0, 5e-3 * 130, (0,0,0), 2)
                cv2.putText(image,'Humans Detected :'+str(counter) ,(10, 50), 0, 5e-3 * 130, (0,0,0), 2)
                cv2.putText(image,localtime,(10, 73), 0, 5e-3 * 130, (0,0,0), 2)  
                x = x                           

        if x == 0 :
            print ("No People Detected " , "Date Time :", localtime)            
                  
        if 0 < x < 2   :
            print ("Humans Detected :" , x , "Date Time :", localtime)
           
        if x >= 2 :
            print ("Too many people !!!!! " , "Date Time :", localtime)
            #line.sendtext('Too many people Noww!!!')
            #line.sendimage(image)   

        fps = 1 / (time.time() - t_start)
        cv2.putText(image, "FPS: {:.2f}".format(fps), (10, 30), 0, 5e-3 * 130, (0,0,255), 2)       
        cv2.imshow("Frame", image)
   
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   

    cap.release()
    cv2.destroyAllWindows()
