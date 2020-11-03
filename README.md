# RoverCam

This is the repository for the video streamer.

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
