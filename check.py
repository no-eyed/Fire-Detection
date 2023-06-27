def check():
    import cv2
    import numpy as np


    net = cv2.dnn.readNet('custom-yolov4-tiny-detector_best.weights', 'custom-yolov4-tiny-detector.cfg')


    classes = []
    with open("classes.txt", "r") as f:
        classes = f.read().splitlines()
    #print(classes)

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(100, 3))

    #filename="prediction.jpg"

    img = cv2.imread("./static/inputs/image.jpg")
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

    #print(classes[indexes])

    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            # label = class_id[i]

            #print(boxes)

            confidence = str(round(confidences[i],2))
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y+20), font, 1, (255,255,255), 2)

            if label == 'fire':
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imwrite('./static/results/boxed_image.jpg', img)
    #cv2.imshow('Image', img)
    #cv2.waitKey(0)

    #cap.release()