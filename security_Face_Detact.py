# -*- coding: utf-8 -*-

import cv2
import numpy as np
import keras
from keras.models import load_model
IMAGE_SIZE = 64

def load_dataset(path_name):
    images, labels = read_path(path_name)
    images = np.array(images, dtype='float')
    labels = np.array([0 if label.endswith('Me') else 1 for label in labels])
    return images, labels

def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)
    h, w, _ = image.shape
    longest_edge = max(h, w)

    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    BLACK = [0, 0, 0]
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
    return cv2.resize(constant, (height, width))


class Model:
    def __init__(self):
        self.model = None

    def load_model(self, file_path):
        self.model = load_model(file_path)

    def face_predict(self, image):
        image = resize_image(image)
        image = image.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))
        image = image.astype('float32')
        image /= 255
        result = self.model.predict(image)
        return result.argmax(axis=-1)

def face_detact():
    me_count = 0
    loop_count = 0
    continuity = 0

    model = Model()
    model.load_model(file_path='./model/me.face.model.h5')
    classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            with open('./txt/security_Flag','w') as f:
                f.write(str(2))
            return 0
        if continuity != me_count:
            continuity = 0
            me_count = 0
        if loop_count == 100:
            cap.release()
            print('you ain\'t the one')
            return 0
        if me_count == 6:
            security_flag = 1
            cap.release()
            print('you are the one!')
            with open('./txt/security_Flag','w') as f:
                f.write(str(1))
            return 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        print(me_count)
        if len(faceRects) > 0:
            for faceRect in faceRects:
                x, y, w, h = faceRect
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                if image is None:
                    break
                else:
                    faceID = model.face_predict(image)
                    if faceID[0] == 0:
                        me_count += 1
                        continuity += 1
                    else:
                        continuity += 1
        loop_count += 1

    cap.release()



if __name__ == '__main__':
    face_detact()
