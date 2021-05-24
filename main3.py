import sys
import time
import numpy as np
import tensorflow as tf
import cv2
import time
from FROZEN_GRAPH_HEAD import TensoflowHeadDector
from parinya import LINE


#import mysql.connector 


#mydb = mysql.connector(
  #  host="locashost",
   # user="root",
   # passed="1234"
#)




# Path โมเดล
PATH_TO_CKPT_HEAD = 'model/HEAD_DETECTION_300x300_ssd_mobilenetv2zaza.pb'
line =LINE('6NKd0tSpKCnpyOXxidyHRmbWAJmiuScGyOQEPhnOQ5X')

#source = 'test_video/123.png'
source = 0

#delay ในการส่งข้อมูลหน่วยวินาที แยกกันกับส่งข้อมูลธรรมดา กับส่งแจ้งเตือนไลน์
time_delay_send_data = 3 
time_delay_send_line = 6 

if __name__ == "__main__":
    tDetector = TensoflowHeadDector(PATH_TO_CKPT_HEAD)
    cap = cv2.VideoCapture(source)
    
    #กำหนดตัวแปล 2 อันเพื่อใช้สร้างเงื่อนไขในการส่งข้อมูล
    global zazazaDATA
    zazazaDATA = 0
    global zazazaLINE
    zazazaLINE = 0
    
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

        #ประกาศตัวแปล counter เพื่อเอามาเก็บจำนวนคน
        global counter  
        counter = 0

        #วนลูปหาหัวคน
        for score, box in zip(scores, boxes):

            #ถ้าเจอหัวก็ทำตามคำสั่งใน if
            if score > 0.7 :
            
                left = int(box[1]*im_width)
                top = int(box[0]*im_height)
                right = int(box[3]*im_width)
                bottom = int(box[2]*im_height)
                box_width = right-left
                box_height = bottom-top
               
                #ตรวจเจอกี่หัวก็บวกตามนั้น
                counter += 1

                #ตีกรอบรอบหัวคนแล้วก็แสดง %
                cv2.putText(image, 'Head: {:.2f}%'.format(score*100), (left, top-5), 0, 5e-3 * 130, (255,0,0),2) 
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), int(round(im_height/150)), 8)
           
           #ถ้า counter อยู่ระหว่าง 0-2 ก็ปริ้นข้อมูลตามนั้น
            elif 0 < counter < 2 and (time.time() - zazazaDATA) > time_delay_send_data:
                zazazaDATA = time.time()
                #ส่งจำนวนคน, เวลา, สถานที่
                print ("Humans Detected :" , counter , "Date Time :", localtime,"Location : Pi 1")
 
            #ถ้า counter เป็น 0 แสดงว่ามันหาหัวไม่เจอก็ปริ้นตามนี้ 
            elif counter == 0 and (time.time() - zazazaDATA) > time_delay_send_data: 
                zazazaDATA = time.time()  
                #ส่งจำนวนคน, เวลา, สถานที่
                print ("Humans Detected :" , counter , "Date Time :", localtime,"Location : Pi 1")           
                
            #ถ้า counter มากกว่า หรือเท่ากับ 2 ก็ปริ้นตามนั้น                                           
            elif counter >= 2 and (time.time() - zazazaLINE) > time_delay_send_line :
                zazazaLINE = time.time()
                #ส่งจำนวนคน, เวลา, สถานที่
                print ("Too many People :" , "Date Time :", localtime,"Location : Pi 1")
                print("Line send !!!")
                #ส่งแจ้งเตือนไลน์
                #line.sendtext('Too many people Noww!!!', localtime, "Location : Pi 1")
                #line.sendimage(image[:, :, ::-1])
                 

        #เอาไว้ put text บนหน้าจอแสดงผลแบบ real time ที่เอาแยกกับด้านบนเพราะว่าอันข่างบน set delay แต่อันนี้ไม่ แปลว่ามันจะแสดงผลบนจอตลอดเวลาเงื่อนไขเหมือนกับข่างบน
        if 0 < counter < 2  :
            cv2.putText(image,'Humans Detected :'+str(counter),(10, 50), 0, 5e-3 * 130, (0,0,0), 2)
            cv2.putText(image,localtime,(10, 73), 0, 5e-3 * 130, (0,0,0), 2)
            cv2.putText(image,'Location : Piv1',(10, 93), 0, 5e-3 * 130, (0,0,0), 2)

        if counter == 0 :
            cv2.putText(image,'Humans Detected :'+str(counter),(10, 50), 0, 5e-3 * 130, (0,0,0), 2)
            cv2.putText(image,localtime,(10, 73), 0, 5e-3 * 130, (0,0,0), 2)
            cv2.putText(image,'Location : Piv1',(10, 93), 0, 5e-3 * 130, (0,0,0), 2)
                    
        if counter >= 2 :
            cv2.putText(image,'Too many people !!!!! ',(10, 113), 0, 5e-3 * 130, (0,0,0), 2)
            cv2.putText(image,'Humans Detected :'+str(counter) ,(10, 50), 0, 5e-3 * 130, (0,0,0), 2)
            cv2.putText(image,localtime,(10, 73), 0, 5e-3 * 130, (0,0,0), 2)  
            cv2.putText(image,'Location : Piv1',(10, 93), 0, 5e-3 * 130, (0,0,0), 2)
           
        fps = 1 / (time.time() - t_start)
        cv2.putText(image, "FPS: {:.2f}".format(fps), (10, 30), 0, 5e-3 * 130, (0,0,255), 2)       
        cv2.imshow("Frame", image)
        
        #กดปุ่ม q เพื่อปิดหน้าต่าง
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   

    cap.release()
    cv2.destroyAllWindows()
