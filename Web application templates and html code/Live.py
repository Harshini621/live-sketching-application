import cv2 as cv
import numpy as np
import os
from flask import Flask, render_template, Response
import socket
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('app.html')

def sketch(image):
    #Converting image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    #cv.imshow('Original image',image)
    #cv.imshow('Gray image', gray)
    
    #cleaning up using gaussian blur
    blur = cv.GaussianBlur(gray,(5,5),0)
    #cv.imshow('Original image',image)
    #cv.imshow('blurred', blur)
    
    #extracting edges using canny edge
    edges = cv.Canny(blur,100,200)
    #cv.imshow('Original image',image)
    #cv.imshow('edge image', edges)
    
    #threshold inversion
    ret, mask = cv.threshold(edges, 70, 255, cv.THRESH_BINARY_INV)
    #cv.imshow('Original image',image)
    #cv.imshow('threshold inversion', mask)
    return mask

def gen():
    camera = cv.VideoCapture(0)

    if not os.path.exists('images'):
        os.makedirs('images')
    i = 0
    while True:
        ret, frame = camera.read()
        if ret == False:
            break
        ##cv.imshow('livesketcher',sketch(frame))
        ##name = './images/frame' + str(i) + '.jpg'
        ##print ('Creating...' + name)
    

        ##cv.imwrite(name, sketch(frame))
        ##i+=1
        img = sketch(frame)
        frame = cv.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        ##time.sleep(0.1)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
    cv.destroyAllWindows()
    camera.release()


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/index_html')
def index_html():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host=local_ip, port=8000)
