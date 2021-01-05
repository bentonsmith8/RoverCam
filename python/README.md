# RoverCam Python

This is the python video streamer. This may or may not work on the rover, it depends on if the dependencies like imutils can run on ARM or not. However, I don't want to babysit the rover for hours trying to do something that may not actually be possible, so instead this method is being deprecated and the video streamer will be rewritten in C++.

That being said, here are the installation instructions.

## Installation

It requires python3 and 3 libraries:

- imutils
- flask
- opencv-contrib-python

install these with

```
pip install imutils flask opencv-contrib-python
```

To run, use

```
python3 client.py -i [ip that you want to run on] -o [port]
```

and navigate to that ip from another device.

---
Note, I ran into an issue with numpy 1.19.4 on Windows where the script would not start. This can be fixed by uninstalling version 1.19.4 and reinstalling version 1.19.3

```
pip uninstall numpy
pip install numpy=1.19.3
```

---
Another note, instead of using pip on its own, 

```
py -m pip install whatever_packages
```

does the same thing and is probably better for some reason.
