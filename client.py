import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import numpy as np
import imutils


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('0.tcp.ngrok.io', 19194))
client_socket.connect(('192.168.50.244', 8485))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

# 設定影像的尺寸大小
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

img_counter = 0

#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
print(encode_param)

while True:
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=320)
    frame = cv2.flip(frame,180)
    result, image = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(image, 0)
    size = len(data)


    # print("{}: {}".format(img_counter, size))
    if img_counter%10==0:
        client_socket.sendall(struct.pack(">L", size) + data)
        cv2.imshow('ImageWindow',frame)
        
    img_counter += 1

    # 若按下 q 鍵則離開迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cam.release()