from signal import signal, SIGINT
from sys import exit
import cv2
import numpy as np
import zmq

def cleanup():
    context.destroy()

def handler(signal_received, frame):
    cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://localhost:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')
socket.setsockopt(zmq.RCVHWM, 1)

while True:
    md = socket.recv_json()
    msg = socket.recv()
    if md['type'] == 'jpg':
        A = np.frombuffer(msg, dtype=np.uint8)
        image = cv2.imdecode(A, 1)
    else:
        A = np.frombuffer(msg, dtype=md['dtype'])
        image = A.reshape(md['shape'])
    cv2.imshow('Video Stream', image)
    cv2.waitKey(1)

context.destroy()