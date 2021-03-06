# RoverCam Python

This is the python video streamer. It requires python3 version >3.8.5, 3 libraries, and creation of a virtual environment ahead of time. This works on the rover with a few extra steps which are detailed below.

## Setting Up A Virtual Environment

To create a virtual environment, first install virtual environments with
```
sudo apt-get install python3-venv
```

Make sure you are in /RoverCam/python then run

```
python3 -m venv .
```

This will create a new virtual environment in /RoverCam/python. The virtual environment must be activated every time the program needs to be run which can be done (on Linux) with:

```
source ./bin/activate
```
---

## Installing Packages

Next, these four packages need to be installed

- wheel
- imutils
- flask
- opencv-contrib-python

install these with

```
pip install wheel opencv-contrib-python flask
```

The imutils package needs to be installed using the flag --no-cache-dir like so:

```
pip install imutils --no-cache-dir
```
---

## Usage
To run, use

```
python3 client.py -i [ip that you want to run on] -o [port] -s [camera index]
```

and navigate to that ip from another device.

---
Note, I ran into an issue with numpy 1.19.4 on Windows where the script would not start. This can be fixed by uninstalling version 1.19.4 and reinstalling version 1.19.3

```
pip uninstall numpy
pip install numpy=1.19.3
```
