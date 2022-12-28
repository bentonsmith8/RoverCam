from signal import signal, SIGINT
from sys import exit

import argparse
import socket
import numpy as np
import cv2
import zmq

class VideoStream:
    def __init__(self, src=0, name='VideoStream'):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        self.grabbed, self.frame = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the thread stop event
        self.stopped = False

    def read(self):
        return self.stream.read()

    def stop(self):
        self.stopped = True

    def close(self):
        self.stream.release()

def encode_jpeg(image, quality):
    return cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1].tostring()


def cleanup():
    cap.close()
    context.destroy()

def handler(signal_received, frame):
    cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

cap = VideoStream(src=0)

green = (0, 255, 0)

i = 0

send_jpg = True

while True:

    i = i + 1
    print(f'Sending image {i}')
    msg = f'Image {i}'

    #open camera
    ret, image = cap.read()

    cv2.putText(image, f'Image {i}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, green, 2, cv2.LINE_AA)

    enc_image = encode_jpeg(image, 50)

    md = dict(
        dtype = str(image.dtype),
        shape = image.shape,
        type = 'jpg' if send_jpg else 'raw',
        msg=msg
    )

    socket.send_json(md, zmq.SNDMORE)
    if send_jpg:
        socket.send(enc_image, zmq.NOBLOCK)
    else:
        socket.send(image, zmq.NOBLOCK)