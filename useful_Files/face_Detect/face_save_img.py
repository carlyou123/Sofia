import cv2

def getTrainingData(window_Name, video_Id, path_Name, max_Num):
    cv2.namedWindow(window_Name)
    cap = cv2.VideoCapture(video_Id)
    classfier = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    color = (0,200,0)
    num = 0
    while cap.isOpened():
        ok,frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceRects = classfier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32,32))
        if len(faceRects)>0:
            for faceRect in faceRects:
                x,y,w,h = faceRect
                image_Name = '%s%d.png' %(path_Name, num)
                image = frame[y:y+h, x:x+w]

                print(image_Name)
                cv2.imwrite(image_Name, image)
                cv2.rectangle(frame,(x-10,y-10),(x+w-10,y+h-10),color,2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, ('%d'%num), (x+30, y+30), font, 1, (100,100,255), 4)
                num +=1
                if num >= max_Num:
                    break
        if num >= max_Num:
            break
        cv2.imshow(window_Name,frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow(window_Name)
    print("detect finished")

if __name__ == '__main__':
    print('face detecting...')
    print('data saving...')
    getTrainingData('facedetecting',0, '.\\training_Data_Me\\', 400)