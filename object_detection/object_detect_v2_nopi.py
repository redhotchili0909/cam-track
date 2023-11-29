import cv2

#This is to pull the information about what each object is called
classNames = []
classFile = "models/coco/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

#This is to pull the information about what each object should look like
configPath = "models/coco/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "models/coco/frozen_inference_graph.pb"

#Set up tracker
tracker = cv2.legacy_TrackerMOSSE.create()
#This is some set up values to get good results
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

#This is to set up what the drawn box size/colour is and the font/size/colour of the name tag and confidence label   
def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
#Below has been commented out, if you want to print each sighting of an object to the console you can uncomment below     
#print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className == "person" or className == "backpack": 
                objectInfo.append([box,className])
                print(box)
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.circle(img,(int((box[0]+box[2])/2), int((box[1]+box[3])/2)), 1, (0,0,255), 1)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+50,box[1]+50), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0],box[1]), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    else:
        box = [1000, 1000, 1000, 1000]
    
    return img,objectInfo,box

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

#Below is the never ending loop that determines what will happen when an object is identified.
frame_count = 0    
while True:
        ret, frame = cap.read()
#Below provides a huge amount of controll. the 0.45 number is the threshold number, the 0.2 number is the nms number)
        if frame_count <= 100:
            result, objectInfo, box = getObjects(frame,0.6,0.2)
        elif frame_count == 101:
            track_result = tracker.init(frame, box)
            box_width = box[2] - box[0]
            box_height = box[3] - box[1]
            
        else:
            track_result, box = tracker.update(frame)
            cv2.rectangle(frame,(int(box[0]), int(box[1])), (int(box[0]+box_width), int(box[1]+box_height)),color=(0,255,0),thickness=2)

        
        #track_result, frame = cap.read()
        #track_result, box = tracker.update(frame)
        #if track_result:
            #cv2.rectangle(frame, box, (0, 0, 255), thickness=2)
        #box[0] -= 300
        #box[2] -= 300
        #box[1] -= 240
        #box[3] -= 240
        #x_coord = (box[0]+box[2])/2
        #y_coord = (box[1]+box[3])/2
        #print([x_coord, y_coord])
        #coords = [x_coord, y_coord]
        #ser.write(coords.encode("utf-8"))
        #line = ser.readline().decode("utf-8").rstrip()
        #print(f"from arduino: {line}")

        #print(objectInfo)
        cv2.imshow("Output",frame)
        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    