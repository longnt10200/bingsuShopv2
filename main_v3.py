import sys
import cv2
from camera import Camera_thread
import threading
import os 
import datetime
from multiprocessing import Process, Queue
import multiprocessing
import logging
import serverApiConst as api
from flask import Flask, render_template, Response
import requests
import time

cam_1 = api.cam_1
cam_2 = api.cam_2

input_cam_1 = Queue(2)
input_cam_2 = Queue(2)

output_cam_1 = Queue(2)
output_cam_2 = Queue(2)

processing_cam1 = None
processing_cam2 = None

FRAME_CAM_1 = None
FRAME_CAM_2 = None


Logging = None
queue_pid = Queue()
ip_camera = Queue()
name_camera = Queue()


app = Flask(__name__)

def read_frame_global():
    global FRAME_CAM_1
    global FRAME_CAM_2
    global input_cam_1, input_cam_2

    while True:
        # print('\n Out Frame \n')
        if not input_cam_1.empty():
            FRAME_CAM_1 = input_cam_1.get()
            # cv2.imwrite('cam1.jpg', FRAME_CAM_1)
        if not input_cam_2.empty():
            FRAME_CAM_2 = input_cam_2.get()
            # cv2.imwrite('cam2.jpg', FRAME_CAM_1)
        

def respones_frame_cam1():
    global FRAME_CAM_1
    while True:
        if FRAME_CAM_1 is not None:
            _, jpg = cv2.imencode('.jpg', FRAME_CAM_1)
            frame = jpg.tostring()
            # cv2.imwrite('cam1.jpg', FRAME_CAM_1)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def respones_frame_cam2():
    global FRAME_CAM_2
    while True:
        if FRAME_CAM_2 is not None:
            _, jpg = cv2.imencode('.jpg', FRAME_CAM_2)
            frame = jpg.tostring()
            # cv2.imwrite('cam2.jpg', FRAME_CAM_1)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def thread_input():
    read_camera = Camera_thread(ip_camera, name_camera)
    Logging.info("Starting processing camera 1")
    thread_cam1 = threading.Thread(name='thread_cam1', target=read_camera.get_frame_camera_rtsp, args=(cam_1, input_cam_1))
    thread_cam1.start()
    Logging.info("Started processing camera 1")
    
    Logging.info("Starting processing camera 2")
    thread_cam2 = threading.Thread(name='thread_cam2', target=read_camera.get_frame_camera_rtsp, args=(cam_2, input_cam_2))
    thread_cam2.start()
    Logging.info("Started processing camera 2")

def thread_output():
    thread_out = threading.Thread(target=read_frame_global)
    thread_out.start()


@app.before_first_request
def start_camera():

    global Logging
    Logging.info("Login to Dsoft-Backend")
    thread_input()

    thread_output()

def auto_start_app():
    def start_loop():
        global Logging

        logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
        Logging = logging.getLogger()
        not_started = True
        Logging.info("Starting flask server ...")
        while not_started:
            try: 
                r = requests.get(api.AI_TRIGGER_START_FLASK)
                if r.status_code == 200:
                    not_started = False
                    Logging.info("Started flask sever!")
            except:
                Logging.error("The Flask server not start yet, keep trying")
            time.sleep(2.0)
    thread = threading.Thread(target=start_loop)
    thread.start()

@app.route('/started', methods=['GET'])
def is_servered():
    return Response(status=200)

@app.route('/video_cam1')
def video_cam1():
    return Response(respones_frame_cam1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_cam2')
def video_cam2():
    return Response(respones_frame_cam2(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    auto_start_app()

    app.run(host=api.API_HOST, port=6600, debug=False)