# Gesture_Volume_Control
Controlling system volume through Hand Gestures


Gesture Volume Control was built with the expectation of helping users having a hard time frequently adjusting their system volume while watching some program(usually the plethora of advertisements during a sports event).


GVC enables the user to <b>adjust the system volume by just gesturing their hands in the view of of the camera.</b>
This helps from having to frequently try and reach the volume button controller on the keyboard.

Also it <b>doesn't cause any volume fluctuation when no hand gesture is made</b>, since it has been designed in such a way that, only if a hand in front of camera is detected, then tracking takes place.


GVC has been built using the Hand Recognition and Tracking software <a href="https://google.github.io/mediapipe/">Mediapipe</a> , <a href="https://opencv.org/">OpenCV</a>, the Python Core Audio Windows Library <a href="https://github.com/AndreMiras/pycaw">Pycaw</a>, Python and Numpy.


It is best when run within a python virtual environment which makes maintaining the different packages easier.


Note: The criteria for adjusting volume based on hand gesture can be modified to suit your needs, since some parameters like the usual distance of your palm from camera while gesturing, your system volume range as detected by Pycaw, might be different for each system.

Files:
 
 * hand_tracker_module.py   -  Module containing Hand Tracking functions.
 * vol_control              -  Script to be run, containing OpenCV methods to receive video input, call tracking module on the frames, and display the output.
