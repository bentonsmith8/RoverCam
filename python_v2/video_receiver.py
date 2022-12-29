from signal import signal, SIGINT
from sys import exit
import cv2
import numpy as np
import zmq
from argparse import ArgumentParser
import time

def cleanup():
    context.destroy()

def handler(signal_received, frame):
    cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)

parser = ArgumentParser()
parser.add_argument('--ip', type=str, default='localhost', help='IP address of the server')
parser.add_argument('--port', type=int, default=5555, help='Port of the server')
args = parser.parse_args()
hostname = 'tcp://{}:{}'.format(args.ip, args.port)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, '')
socket.setsockopt(zmq.RCVHWM, 1)
socket.setsockopt(zmq.RCVBUF, 0)
# socket.setsockopt(zmq.CONFLATE, 1)
socket.connect(hostname)

current_time = last_time = time.perf_counter()

while True:
    current_time = time.perf_counter()
    time_diff = current_time - last_time
    last_time = current_time
    fps = 1 / time_diff
    print('FPS: {0:2.2f}'.format(fps), end='\t')
    start = time.perf_counter()
    md = socket.recv_json()
    msg = socket.recv()
    end = time.perf_counter()
    print('Time to receive: {0:3.2f} ms'.format((end - start) * 1000), end='\t')
    start = time.perf_counter()
    if md['type'] == 'jpg':
        A = np.frombuffer(msg, dtype=np.uint8)
        image = cv2.imdecode(A, 1)
    else:
        A = np.frombuffer(msg, dtype=md['dtype'])
        image = A.reshape(md['shape'])
    end = time.perf_counter()
    print('Time to decode: {0:3.2f} ms'.format((end - start) * 1000))
    cv2.imshow('Video Stream', image)
    cv2.waitKey(1)

context.destroy()