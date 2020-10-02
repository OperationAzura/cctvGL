#import demo
import pi3d
#import sys
#sys.path.insert(1, '/home/pi/pi3d')

import numpy as np
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera

import time

import cv2

rot = 36
rotCh = 1
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 1
camera.crop = (0.0, 0.0, 2.0, 2.0)
#camera.hflip = True
rawCapture = PiRGBArray(camera, (480, 320))
#camera.crop = (0.0, 0.0, 1.0, 1.0)
time.sleep(0.1)

#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#    image = frame.array

DISPLAY = pi3d.Display.create(x=50, y=50, frames_per_second=30, display_config=pi3d.DISPLAY_CONFIG_FULLSCREEN)
shader = pi3d.Shader("uv_flat")
CAMERA = pi3d.Camera(is_3d=False)
tex = pi3d.Texture(Image.open('img.jpg'))
sprite = pi3d.ImageSprite(tex, shader, w=480.0, h=320.0, z=5.0)
xloc = 100
yloc = 100
count = 0
#start = time.clock()
for frame in camera.capture_continuous(rawCapture, format="bgr", resize=(480,320), use_video_port=True):
    start = time.clock()
    count += 1
    #pi3d.TextureCache().clear()
    #rawCapture.truncate(0)
    #rawCapture.seek(0)
    #print('how many times?')
    tex = pi3d.Texture(frame.array, flip=True)
    #tex._unload_opengl()
    #tex.update_ndarray(frame.array)
    #tex.image = frame.array
    #tex._load_opengl()
    #sprite.draw()
    #time.sleep(1)
    rawCapture.truncate(0)
    sprite = pi3d.ImageSprite(tex, shader, w=480.0, h=320.0, z=5.0)
    #rawCapture.truncate(0)
    mykeys = pi3d.Keyboard()
    #xloc = 100.0
    dx = 2.3
    #yloc = 100.0
    dy = 1.23
    if DISPLAY.loop_running():
        #sprite.draw()
        sprite.rotateIncZ(rot)
        rot += rotCh
        sprite.position(xloc, yloc, 5.0)
        sprite.draw()
        if xloc > 640.0:
            dx = -2.7
        elif xloc < -640.0:
            dx = 2.5
        if yloc > 640.0:
            dy = -1.23
        elif yloc < -640.0:
            dy = 1.23
        xloc += dx
        yloc += dy
  
        if mykeys.read() == 27:
            print('XXXXXXXXXXX')
            print('avg process time per frame: ',float(time.clock() - start)/count/1000)
            mykeys.close()
            DISPLAY.destroy()
            #print('XXXXXXXXXXX')
            #print(float(time.clock() - start)/count)
        print('farme time: ',  start / 1000)
    else:
        camera.close()
        rawCapture.close()
