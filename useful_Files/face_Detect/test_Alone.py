# -*- coding: utf-8 -*-

import cv2
import numpy as np
from keras.models import load_model
IMAGE_SIZE = 64

def load_dataset(path_name):
    images, labels = read_path(path_name)
    # 将lsit转换为numpy array
    images = np.array(images, dtype='float')  # 注意这里要将数据类型设为float，否则后面face_train_keras.py里图像归一化的时候会报错，TypeError: No loop matching the specified signature and casting was found for ufunc true_divide

    #    print(images.shape) # (1969, 64, 64, 3)
    # 标注数据，me文件夹下是我，指定为0，其他指定为1，这里的0和1不是logistic regression二分类输出下的0和1，而是softmax下的多分类的类别
    labels = np.array([0 if label.endswith('Me') else 1 for label in labels])
    return images, labels

def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图片尺寸
    h, w, _ = image.shape

    # 对于长宽不等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多少像素宽度才能与长边等长(相当于padding，长边的padding为0，短边才会有padding)
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass  # pass是空语句，是为了保持程序结构的完整性。pass不做任何事情，一般用做占位语句。

    # RGB颜色
    BLACK = [0, 0, 0]
    # 给图片增加padding，使图片长、宽相等
    # top, bottom, left, right分别是各个边界的宽度，cv2.BORDER_CONSTANT是一种border type，表示用相同的颜色填充
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)
    # 调整图像大小并返回图像，目的是减少计算量和内存占用，提升训练速度
    return cv2.resize(constant, (height, width))


class Model:
    # 初始化构造方法
    def __init__(self):
        self.model = None

    def load_model(self, file_path):
        self.model = load_model(file_path)

    def face_predict(self, image):
        # 将探测到的人脸reshape为符合输入要求的尺寸
        image = resize_image(image)
        image = image.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))
        # 图片浮点化并归一化
        image = image.astype('float32')  # float32	Single precision float: sign bit, 8 bits exponent, 23 bits mantissa
        image /= 255
        result = self.model.predict(image)
        #        print('result:', result)
        #        print(result.shape) # (1,2)
        #        print(type(result)) # <class 'numpy.ndarray'>
        return result.argmax(axis=-1)  # The axis=-1 in numpy corresponds to the last dimension



# 加载模型
model = Model()
model.load_model(file_path='./model/me.face.model.h5')

# 框住人脸的矩形边框颜色
cv2.namedWindow('Detecting your face.')  # 创建窗口
color = (0, 255, 0)
classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')  # 加载分类器
# 捕获指定摄像头的实时视频流
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ok, frame = cap.read()  # type(frame) <class 'numpy.ndarray'>
    if not ok:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 灰度化
    faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    if len(faceRects) > 0:
        for faceRect in faceRects:
            x, y, w, h = faceRect

            # 截取脸部图像提交给模型识别这是谁
            image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
            if image is None:  # 有的时候可能是人脸探测有问题，会报错 error (-215) ssize.width > 0 && ssize.height > 0 in function cv::resize，所以这里要判断一下image是不是None，防止极端情况 https://blog.csdn.net/qq_30214939/article/details/77432167
                break
            else:
                faceID = model.face_predict(image)
                #                print(faceID) # [0]
                #                print(type(faceID)) # <class 'numpy.ndarray'>
                #                print(faceID.shape) # (1,)
                #                #如果是“我”
                if faceID[0] == 0:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)

                    # 文字提示是谁
                    cv2.putText(frame, 'Carl',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (255, 0, 20),  # 颜色
                                2)  # 字的线宽
                else:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
                    # 文字提示是谁
                    cv2.putText(frame, 'Somebody else I don\'t care',
                                (x + 30, y + 30),  # 坐标
                                cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                                1,  # 字号
                                (20, 0, 255),  # 颜色
                                2)  # 字的线宽
    cv2.imshow("Detecting your face.", frame)

    # 等待10毫秒看是否有按键输入
    k = cv2.waitKey(10)
    # 如果输入q则退出循环
    if k & 0xFF == ord('q'):
        break

# 释放摄像头并销毁所有窗口
cap.release()
cv2.destroyAllWindows()
print('face detect finished!')