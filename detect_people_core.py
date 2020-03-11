import cv2
from detectPeoplev5 import detect_people
import logging 
import sys
import collections
import multiprocessing
from multiprocessing import Process 
import threading
import datetime
import serverApiConst as api
from postdatabase import postdata

Logging = None

count_frame = 1
list_id = None

logging.basicConfig(format= "[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
Logging = logging.getLogger()
def run(input_queue, direction, output_queue, model, queue_pid):
    global Logging
    global count_frame, list_id

    time_now = api.timeline.copy()
    Logging.info("Get frame from {}".format(direction))

    if direction == 'cam1':
        pid = multiprocessing.current_process().pid
        dict_pid = {'cam1': pid}
        queue_pid.put(dict_pid)
    
    elif direction == 'cam2':
        pid = multiprocessing.current_process().pid
        dict_pid = {'cam2': pid}
        queue_pid.put(dict_pid)

        while True:

            if not input_queue.empty():
                frame = input_queue.get()
                height, width = frame.shape[:2]
            else: 
                continue
            now = datetime.datetime.now()
            BG = model.processing(frame)
            output_queue.put(BG)
            if now.hour in time_now:
                data =  r'{"time": "' + now.strftime("%Y-%m-%d") + r' ' + str(now.hour -1)+ r':00'  + r'","count":' + str(len(model.ID)) + r',"id_store":' + str(direction) + r'}'
                # postdata(data)
                Logging.info(data)
                time_now.pop(time_now.index(now.hour))
                model.ID = []
            if time_now == []:
                time_now = api.timeline.copy()
            
