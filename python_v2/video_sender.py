import argparse
import socket
from signal import SIGINT, signal
from sys import exit
import time

import cv2
import numpy as np
import zmq

WIDTH = 1280
HEIGHT = 720


class VideoStream:
    '''
    Class to handle video streaming from a camera
    '''
    def __init__(self, src=0, name='VideoStream'):
        # initialize the video camera stream and set the
        # frame size and encoding
        self.src = src
        self._get_stream(src)

        # initialize the stream name
        self.name = name

        # initialize the capture stop event
        self.stopped = False

        self.error = False

    def _get_stream(self, src=0):
        # return the video camera stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.stream.set(cv2.CAP_PROP_FOURCC,
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


    def read(self):
        # return the frame most recently read
        grabbed, frame = self.stream.read()
        if grabbed:
            return frame

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def close(self):
        self.stream.release()


def encode_jpeg(image, quality):
    '''
    Encode an image as a jpeg
    
    Args:
        image: the image to encode
        quality: the quality of the image (0-100)
        
    Returns:
        the encoded image
    '''
    return cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1].tobytes()


def cleanup():
    cap.close()
    context.destroy()


def handler(signal_received, frame):
    cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

# bind the handler to SIGINT
signal(SIGINT, handler)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, default="*",
                help="ip address of the device")
ap.add_argument("-o", "--port", type=int, default=5555,
                help="ephemeral port number of the server (1024 to 65535)")
args = vars(ap.parse_args())

hostname = 'tcp://{}:{}'.format(args['ip'], args['port'])

# create the zmq context and socket
# note, the zmq context only needs to be created once but it
# can create multiple sockets
context = zmq.Context()
# create a publisher socket
socket = context.socket(zmq.PUB)
# set the high water mark to 2
# this means that if the subscriber is not receiving messages
# the publisher will drop all messages that are not the current frame
socket.setsockopt(zmq.SNDHWM, 2)
socket.setsockopt(zmq.RCVHWM, 2)
# set linger to 0
# this means that if the video stream is closed it won't try to deliver 
# any messages that are still in the queue
# socket.setsockopt(zmq.LINGER, 0)
# set immediate to 1
# this will only queue messages if the subscriber is ready to receive them
# socket.setsockopt(zmq.IMMEDIATE, 1)
socket.bind(hostname)

cap = VideoStream(src=0)

green = (0, 255, 0)

i = 0

send_jpg = True

while True:
    i = i + 1
    print(f'Sending image {i}')
    msg = f'Image {i}'

    # open camera
    image = cap.read()

    if image is None:
        print('No image')
        continue

    # add text to image
    cv2.putText(image, f'Image {i}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, green, 2, cv2.LINE_AA)


    # create metadata
    md = dict(
        dtype=str(image.dtype),
        shape=image.shape,
        type='jpg' if send_jpg else 'raw',
        msg=msg
    )

    # send the metadata about the image first
    socket.send_json(md, zmq.SNDMORE)

    # send the image
    if send_jpg:
        # encode the image as a jpeg
        enc_image = encode_jpeg(image, 20)
        socket.send(enc_image, zmq.NOBLOCK)
    else:
        socket.send(image, zmq.NOBLOCK)