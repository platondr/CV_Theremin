CV Theremin
The project creates a theremin, using computer vision
The theremin creates sound based on the position of the index fingers of both hands (the hand to the left controls volume, the hand to the right controls the pitch of the sound)
The interface shows the lines, that represent the arms of a real-life theremin - one for volume (the closer to it the hand gets, the quieter the theremin is) and one for the pitch (the closer to the line the hand gets, the higher the pitch)

The project requires the libraries from 'requirements.txt' to be installed

To run the project, you must install these libraries and start the 'main.py' file, to close it, you should stop 'main.py'.

The theremin is a fun thing to mess around with, however it can also be used to record interesting sounds.
Currently, the project is finished
You can contact the creator via GitHub (@platondr) of email (platon.drozman@gmail.com)

### Suggestions from Misyriy Andreev:
- Writing a good README.md file. The current one lacks information, lacks usage examples, lacks installation instructions, etc. + explain what a theremin is
- Drawing the volume and pitch axes on the screen. Writing that in README is not enough
- Making the code terminate when the window is closed
BUG:
if you terminate the code, then run it, close the window and terminate the code again, you get KeyboardInterrupt error from mediapipe
