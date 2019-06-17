#!/usr/bin/python
# -*- coding: utf-8 -*-
# --- Author: YAOLINJUN
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import numpy as np
import csv
import time
import _thread
import threading
import tkinter.filedialog, tkinter.messagebox
import tkinter as tk
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
import sqlite3
import os
from PIL import ImageTk
import PIL.Image

# Object detection imports
from utils import label_map_util
from utils import visualization_utils as vis_util
from utils.color_recognition_module import color_recognition_api
from utils.vehicle_detection_module import vehicle_detection_api
from utils.vehicle_detection_module.vehicle_detection_api import *
from utils.image_utils import image_saver
from tkinter import *           
from tkinter import ttk,Entry,Label,LabelFrame

MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = \
    'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

#position of interest area : Tensorflow only recognize the vehicle in interest area
INTEREST_AREA_X_START=300
INTEREST_AREA_Y_START=420
INTEREST_AREA_X_END=1700
INTEREST_AREA_Y_END=1060

##position of the roi area(only when the position of the car is between ROI_TOP_POSITION and ROI_BOTTOM_POSSTION will it be detected by vehicle_detection_api
#ROI_TOP_POSITION = INTEREST_AREA_Y_START
#ROI_BOTTOM_POSITION = INTEREST_AREA_Y_END

IS_LANE_FIRST_AVAILABLE=True
IS_LANE_SECOND_AVAILABLE=True
IS_LANE_THIRD_AVAILABLE=True
#the area of the line_crossing detection line height=LINE_CROSSING_DETECTION_POS_BOTTOM-LINE_CROSSING_DETECTION_POS_TOP
LINE_CROSSING_DETECTION_POS_TOP=0
LINE_CROSSING_DETECTION_POS_BOTTOM=0

LINE_CROSSING_DETECTION_POS_LEFT=0
LINE_CROSSING_DETECTION_POS_RIGHT=0
#As the line_crossing ROI has a width, the same vehicle may be detected in consecutive frames and therefore,will lead to
#store multiple repeative car image.As a result,the interval(based on the current frame number)is needed
LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE=6
#the area of traffic light :suppose only detecting one light [125:140,895:915]
OFFSET=6 
TRAFFIC_LIGHT_POS_TOP=124
TRAFFIC_LIGHT_POS_BOTTOM=144
TRAFFIC_LIGHT_POS_LEFT=890
TRAFFIC_LIGHT_POS_RIGHT=920

DETECTED_LIGHT_COLOR='green'#default color
#roi pos of lane first START:Xstart END:Xend

LEFT_DETECTION_POSITION_LANE_FIRST_START=0
LEFT_DETECTION_POSITION_LANE_FIRST_END=0
RIGHT_DETECTION_POSITION_LANE_FIRST_START=0
RIGHT_DETECTION_POSITION_LANE_FIRST_END=0
#roi pos of lane second START:Xstart END:Xend
LEFT_DETECTION_POSITION_LANE_SECOND_START=0
LEFT_DETECTION_POSITION_LANE_SECOND_END=0
RIGHT_DETECTION_POSITION_LANE_SECOND_START=0
RIGHT_DETECTION_POSITION_LANE_SECOND_END=0

#roi pos of lane third START:Xstart END:Xend
LEFT_DETECTION_POSITION_LANE_THIRD_START=0
LEFT_DETECTION_POSITION_LANE_THIRD_END=0
RIGHT_DETECTION_POSITION_LANE_THIRD_START=0
RIGHT_DETECTION_POSITION_LANE_THIRD_END=0

#the width of the speed detection roi TOP:Ystart BOTTOM:Yend
SPEED_DETECTION_POSITION_LANE_TOP=670
SPEED_DETECTION_POSITION_LANE_BOTTOM=740
#roi pos of lane first LEFT:Xstart RIGHT:Xend
LEFT_SPEED_DETECTION_POSITION_LANE_FIRST=450
RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST=800
#roi pos of lane second LEFT:Xstart RIGHT:Xend
LEFT_SPEED_DETECTION_POSITION_LANE_SECOND=850
RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND=1200
#roi pos of lane third LEFT:Xstart RIGHT:Xend
LEFT_SPEED_DETECTION_POSITION_LANE_THIRD=1250
RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD=1600


#detect whether the car has leave in order to calculate the speed more accurately
LEAVE_SPEED_DETECTION_POSITION_LANE_TOP=0
LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM=0

DETECTION_LINE_HEIGHT=LINE_CROSSING_DETECTION_POS_TOP
DETECTION_LINE_HEIGHT_END=DETECTION_LINE_HEIGHT+300
#the vehicle speed that over the SPEED_LIMIT will be captured
SPEED_LIMIT=30
#convert piexl to real length in order to calculate the vehicle speed (suppose 1pixel~=0.02m)
PIXEL_TO_REAL_LENGTH=0.02 
PIXEL_HEIGHT_COMPENSATE=0.0001

LINE_BOTTOM_HEIGHT=300

CURRENT_PATH=os.getcwd()

VIDEO_FILE_PATH=CURRENT_PATH+'/videos/'+'video-01.avi'

VIDEO_FILE_NAME='video-01'

roi_configuration_info=''

TOTAL_PASSED_VEHICLE_COUNT=0
font = cv2.FONT_HERSHEY_SIMPLEX
def activate_database():
    database_window  = VehicleInfo()
#    vehicles_info()
    
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Vehicle Detection System')
        self.set_ui()
    def open_database(self):
        database_wind=DatabaseUI()
        print(type(database_wind))
        self.wait_window(database_wind)
    def set_ui(self):
     global interest_area_x_start
     global interest_area_y_start
     global interest_area_x_end
     global interest_area_y_end
     global is_lane_first_available
     global is_lane_second_available
     global is_lane_third_available
     global line_crossing_detection_pos_left
     global line_crossing_detection_pos_right
     global line_crossing_detection_pos_top
     global line_crossing_detection_pos_bottom
     global left_detection_position_lane_first_start
     global left_detection_position_lane_first_end
     global right_detection_position_lane_first_start
     global right_detection_position_lane_first_end
     global left_detection_position_lane_second_start
     global left_detection_position_lane_second_end
     global right_detection_position_lane_second_start
     global right_detection_position_lane_second_end
     global left_detection_position_lane_third_start
     global left_detection_position_lane_third_end
     global right_detection_position_lane_third_start
     global right_detection_position_lane_third_end
     global speed_detection_position_lane_top
     global speed_detection_position_lane_bottom
     global left_speed_detection_position_lane_first
     global right_speed_detection_position_lane_first
     global left_speed_detection_position_lane_second
     global right_speed_detection_position_lane_second
     global left_speed_detection_position_lane_third
     global right_speed_detection_position_lane_third
     global speed_limit
     global pixel_to_real_length
     global pixel_height_compensate
     global light_detected_color
     global traffic_light_pos_top
     global traffic_light_pos_bottom
     global traffic_light_pos_left
     global traffic_light_pos_right
     global leave_speed_detection_position_lane_top
     global leave_speed_detection_position_lane_bottom
     global line_crossing_detection_interval_in_each_lane
     
     
     global is_roi_preview_activated
     
     interest_area_x_start=IntVar()
     interest_area_y_start=IntVar()
     interest_area_x_end=IntVar()
     interest_area_y_end=IntVar()
     
     is_lane_first_available = BooleanVar()
     is_lane_second_available = BooleanVar()
     is_lane_third_available = BooleanVar()
     
     line_crossing_detection_pos_left=IntVar()
     line_crossing_detection_pos_right=IntVar()
     line_crossing_detection_pos_top=IntVar()
     line_crossing_detection_pos_bottom=IntVar()
     
     left_detection_position_lane_first_start=IntVar()
     left_detection_position_lane_first_end=IntVar()
     right_detection_position_lane_first_start=IntVar()
     right_detection_position_lane_first_end=IntVar()
     
     left_detection_position_lane_second_start=IntVar()
     left_detection_position_lane_second_end=IntVar()
     right_detection_position_lane_second_start=IntVar()
     right_detection_position_lane_second_end=IntVar()
     
     left_detection_position_lane_third_start=IntVar()
     left_detection_position_lane_third_end=IntVar()
     right_detection_position_lane_third_start=IntVar()
     right_detection_position_lane_third_end=IntVar()
     
     speed_detection_position_lane_top=IntVar()
     speed_detection_position_lane_bottom=IntVar()    
     left_speed_detection_position_lane_first=IntVar()
     right_speed_detection_position_lane_first=IntVar()
     left_speed_detection_position_lane_second=IntVar()
     right_speed_detection_position_lane_second=IntVar()
     left_speed_detection_position_lane_third=IntVar()
     right_speed_detection_position_lane_third=IntVar()

     speed_limit=IntVar()
     pixel_to_real_length=DoubleVar()
     pixel_height_compensate=DoubleVar()
     
     light_detected_color=StringVar()
     traffic_light_pos_top=IntVar()
     traffic_light_pos_bottom=IntVar()
     traffic_light_pos_left=IntVar()
     traffic_light_pos_right=IntVar()
  
     leave_speed_detection_position_lane_top=IntVar()
     leave_speed_detection_position_lane_bottom=IntVar()
     
     line_crossing_detection_interval_in_each_lane=IntVar()
     
     is_roi_preview_activated = BooleanVar()
     #set value
     interest_area_x_start.set(INTEREST_AREA_X_START)
     interest_area_y_start.set(INTEREST_AREA_Y_START)
     interest_area_x_end.set(INTEREST_AREA_X_END)
     interest_area_y_end.set(INTEREST_AREA_Y_END)    
     
     line_crossing_detection_pos_left.set(LINE_CROSSING_DETECTION_POS_LEFT)
     line_crossing_detection_pos_right.set(LINE_CROSSING_DETECTION_POS_RIGHT)  
     line_crossing_detection_pos_top.set(LINE_CROSSING_DETECTION_POS_TOP)
     line_crossing_detection_pos_bottom.set(LINE_CROSSING_DETECTION_POS_BOTTOM)
     
     is_lane_first_available.set(IS_LANE_FIRST_AVAILABLE)
     is_lane_second_available.set(IS_LANE_SECOND_AVAILABLE)
     is_lane_third_available.set(IS_LANE_THIRD_AVAILABLE)
     
     left_detection_position_lane_first_start.set(LEFT_DETECTION_POSITION_LANE_FIRST_START)
     left_detection_position_lane_first_end.set(LEFT_DETECTION_POSITION_LANE_FIRST_END)
     right_detection_position_lane_first_start.set(RIGHT_DETECTION_POSITION_LANE_FIRST_START)
     right_detection_position_lane_first_end.set(RIGHT_DETECTION_POSITION_LANE_FIRST_END)

     left_detection_position_lane_second_start.set(LEFT_DETECTION_POSITION_LANE_SECOND_START)
     left_detection_position_lane_second_end.set(LEFT_DETECTION_POSITION_LANE_SECOND_END)
     right_detection_position_lane_second_start.set(RIGHT_DETECTION_POSITION_LANE_SECOND_START)
     right_detection_position_lane_second_end.set(RIGHT_DETECTION_POSITION_LANE_SECOND_END)
     
     left_detection_position_lane_third_start.set(LEFT_DETECTION_POSITION_LANE_THIRD_START)
     left_detection_position_lane_third_end.set(LEFT_DETECTION_POSITION_LANE_THIRD_END)
     right_detection_position_lane_third_start.set(RIGHT_DETECTION_POSITION_LANE_THIRD_START)
     right_detection_position_lane_third_end.set(RIGHT_DETECTION_POSITION_LANE_THIRD_END)
     
     
     speed_detection_position_lane_top.set(SPEED_DETECTION_POSITION_LANE_TOP)
     speed_detection_position_lane_bottom.set(SPEED_DETECTION_POSITION_LANE_BOTTOM)  
     left_speed_detection_position_lane_first.set(LEFT_SPEED_DETECTION_POSITION_LANE_FIRST)
     right_speed_detection_position_lane_first.set(RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST)
     left_speed_detection_position_lane_second.set(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND)
     right_speed_detection_position_lane_second.set(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND)
     left_speed_detection_position_lane_third.set(LEFT_SPEED_DETECTION_POSITION_LANE_THIRD)
     right_speed_detection_position_lane_third.set(RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD)
     
     leave_speed_detection_position_lane_top.set(LEAVE_SPEED_DETECTION_POSITION_LANE_TOP)
     leave_speed_detection_position_lane_bottom.set(LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM)
     
     speed_limit.set(SPEED_LIMIT)
     
     pixel_to_real_length.set(PIXEL_TO_REAL_LENGTH)
     pixel_height_compensate.set(PIXEL_HEIGHT_COMPENSATE)
     
     light_detected_color.set(DETECTED_LIGHT_COLOR)
     traffic_light_pos_top.set(TRAFFIC_LIGHT_POS_TOP)
     traffic_light_pos_bottom.set(TRAFFIC_LIGHT_POS_BOTTOM)
     traffic_light_pos_left.set(TRAFFIC_LIGHT_POS_LEFT)
     traffic_light_pos_right.set(TRAFFIC_LIGHT_POS_RIGHT)     
     
     line_crossing_detection_interval_in_each_lane.set(LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE)
     
     
     is_roi_preview_activated.set(False)
     #declare widget variable
     interest_area_x_start_label = Label(self,text='interest_area_x_start',background = 'yellow')
     interest_area_x_start_box = Entry(self,textvariable=interest_area_x_start,width=4)
     interest_area_y_start_label = Label(self,text='interest_area_y_start',background = 'yellow')
     interest_area_y_start_box = Entry(self,textvariable=interest_area_y_start,width=4)
     interest_area_x_end_label = Label(self,text='interest_area_x_end',background = 'yellow')
     interest_area_x_end_box = Entry(self,textvariable=interest_area_x_end,width=4)
     interest_area_y_end_label=Label(self,text='interest_area_y_end',background = 'yellow')
     interest_area_y_end_box = Entry(self,textvariable=interest_area_y_end,width=4)
     
     line_crossing_detection_pos_left_label=Label(self,text='line_crossing_detect_pos_left',background = 'GreenYellow')
     line_crossing_detection_pos_left_box=Entry(self,textvariable=line_crossing_detection_pos_left,width=4)
     line_crossing_detection_pos_right_label=Label(self,text='line_crossing_detect_pos_right',background = 'GreenYellow')
     line_crossing_detection_pos_right_box=Entry(self,textvariable=line_crossing_detection_pos_right,width=4)
     line_crossing_detection_pos_top_label=Label(self,text='line_crossing_detect_pos_top',background = 'GreenYellow')
     line_crossing_detection_pos_top_box=Entry(self,textvariable=line_crossing_detection_pos_top,width=4)
     line_crossing_detection_pos_bottom_label=Label(self,text='line_crossing_detect_pos_bottom',background = 'GreenYellow')
     line_crossing_detection_pos_bottom_box=Entry(self,textvariable=line_crossing_detection_pos_bottom,width=4)
     
     is_lane_first_available_box = Checkbutton(self,text='is_lane_first_available',variable=is_lane_first_available,background = 'LemonChiffon')
     is_lane_second_available_box = Checkbutton(self,text='is_lane_second_available',variable=is_lane_second_available,background = 'LemonChiffon')
     is_lane_third_available_box = Checkbutton(self,text='is_lane_third_available',variable=is_lane_third_available,background = 'LemonChiffon')
     
     left_detection_position_lane_first_start_label=Label(self,text='left_first_start')
     left_detection_position_lane_first_start_box=Entry(self,textvariable=left_detection_position_lane_first_start,width=4)
     left_detection_position_lane_first_end_label=Label(self,text='left_first_end')
     left_detection_position_lane_first_end_box=Entry(self,textvariable=left_detection_position_lane_first_end,width=4)
     right_detection_position_lane_first_start_label=Label(self,text='right_first_start')
     right_detection_position_lane_first_start_box=Entry(self,textvariable=right_detection_position_lane_first_start,width=4)
     right_detection_position_lane_first_end_label=Label(self,text='right_first_end')
     right_detection_position_lane_first_end_box=Entry(self,textvariable=right_detection_position_lane_first_end,width=4)
     
     left_detection_position_lane_second_start_label=Label(self,text='left_second_start')
     left_detection_position_lane_second_start_box=Entry(self,textvariable=left_detection_position_lane_second_start,width=4)
     left_detection_position_lane_second_end_label=Label(self,text='left_second_end')
     left_detection_position_lane_second_end_box=Entry(self,textvariable=left_detection_position_lane_second_end,width=4)
     right_detection_position_lane_second_start_label=Label(self,text='right_second_start')
     right_detection_position_lane_second_start_box=Entry(self,textvariable=right_detection_position_lane_second_start,width=4)
     right_detection_position_lane_second_end_label=Label(self,text='right_second_end')
     right_detection_position_lane_second_end_box=Entry(self,textvariable=right_detection_position_lane_second_end,width=4)
     
     left_detection_position_lane_third_start_label=Label(self,text='left_third_start')
     left_detection_position_lane_third_start_box=Entry(self,textvariable=left_detection_position_lane_third_start,width=4)
     left_detection_position_lane_third_end_label=Label(self,text='left_third_end')
     left_detection_position_lane_third_end_box=Entry(self,textvariable=left_detection_position_lane_third_end,width=4)
     right_detection_position_lane_third_start_label=Label(self,text='right_third_start')
     right_detection_position_lane_third_start_box=Entry(self,textvariable=right_detection_position_lane_third_start,width=4)
     right_detection_position_lane_third_end_label=Label(self,text='right_third_end')
     right_detection_position_lane_third_end_box=Entry(self,textvariable=right_detection_position_lane_third_end,width=4)
     
     speed_detection_position_lane_top_label=Label(self,text='speed_detect_top',background='Olive')
     speed_detection_position_lane_top_box=Entry(self,textvariable=speed_detection_position_lane_top,width=4)
     speed_detection_position_lane_bottom_label=Label(self,text='speed_detect_bottom',background='Olive')
     speed_detection_position_lane_bottom_box=Entry(self,textvariable=speed_detection_position_lane_bottom,width=4)
     left_speed_detection_position_lane_first_label=Label(self,text='speed_first_left',background='Olive')
     left_speed_detection_position_lane_first_box=Entry(self,textvariable=left_speed_detection_position_lane_first,width=4)
     right_speed_detection_position_lane_first_label=Label(self,text='speed_first_right',background='Olive')
     right_speed_detection_position_lane_first_box=Entry(self,textvariable=right_speed_detection_position_lane_first,width=4)
     left_speed_detection_position_lane_second_label=Label(self,text='speed_second_left',background='Olive')
     left_speed_detection_position_lane_second_box=Entry(self,textvariable=left_speed_detection_position_lane_second,width=4)
     right_speed_detection_position_lane_second_label=Label(self,text='speed_second_right',background='Olive')
     right_speed_detection_position_lane_second_box=Entry(self,textvariable=right_speed_detection_position_lane_second,width=4)
     left_speed_detection_position_lane_third_label=Label(self,text='speed_third_left',background='Olive')
     left_speed_detection_position_lane_third_box=Entry(self,textvariable=left_speed_detection_position_lane_third,width=4)
     right_speed_detection_position_lane_third_label=Label(self,text='speed_third_right',background='Olive')
     right_speed_detection_position_lane_third_box=Entry(self,textvariable=right_speed_detection_position_lane_third,width=4)   
     
     leave_speed_detection_position_lane_top_label=Label(self,text='leave_detect_top',background ='IndianRed')
     leave_speed_detection_position_lane_top_box=Entry(self,textvariable=leave_speed_detection_position_lane_top,width=4)
     leave_speed_detection_position_lane_bottom_label=Label(self,text='leave_detect_bottom',background ='IndianRed')
     leave_speed_detection_position_lane_bottom_box=Entry(self,textvariable=leave_speed_detection_position_lane_bottom,width=4)
     
     speed_limit_label_label=Label(self,text='speed_limit',background ='LemonChiffon')
     speed_limit_label_box=Entry(self,textvariable=speed_limit,width=4)
     
     pixel_to_real_length_label=Label(self,text='pixel_to_real_length',background ='LemonChiffon')
     pixel_to_real_length_box=Entry(self,textvariable=pixel_to_real_length,width=6)
     pixel_height_compensate_label=Label(self,text='pixel_height_compensate',background ='LemonChiffon')
     pixel_height_compensate_box=Entry(self,textvariable=pixel_height_compensate,width=6)
     
     light_detected_color_label=Label(self,text='light_detected_color',background ='GreenYellow')
     light_detected_color_box=Entry(self,textvariable=light_detected_color,width=8)
     traffic_light_pos_top_label=Label(self,text='detected_light_color_pos_top',background ='GreenYellow')
     traffic_light_pos_top_box=Entry(self,textvariable=traffic_light_pos_top,width=4)
     traffic_light_pos_bottom_label=Label(self,text='detected_light_color_pos_bottom',background ='GreenYellow')
     traffic_light_pos_bottom_box=Entry(self,textvariable=traffic_light_pos_bottom,width=4)
     traffic_light_pos_left_label=Label(self,text='detected_light_color_pos_left',background ='GreenYellow')
     traffic_light_pos_left_box=Entry(self,textvariable=traffic_light_pos_left,width=4)
     traffic_light_pos_right_label=Label(self,text='detected_light_color_pos_right',background ='GreenYellow')
     traffic_light_pos_right_box=Entry(self,textvariable=traffic_light_pos_right,width=4)
     
     line_crossing_detection_interval_in_each_lane_label=Label(self,text='lane_line_crossing_detection_interval_in_each_lane',background ='LemonChiffon')
     line_crossing_detection_interval_in_each_lane_box=Entry(self,textvariable= line_crossing_detection_interval_in_each_lane,width=8)
     
     button_roi_configuration_load = Button(self, text="load_roi_configuration", command=load_roi_configuration,background='SkyBlue')
     button_roi_configuration_save = Button(self, text="save_roi_configuration", command=save_roi_configuration,background='SkyBlue')
     button_video_file_choose = Button(self, text="Choose Video File", command=get_file_name,bg='SkyBlue',background='SkyBlue')
     button_video_detection= Button(self, text="Run Video Detection", command=object_detection_function,background='SkyBlue')
     
     button_activate_database_ui=Button(self, text="Open Database UI", command=self.open_database,background='SkyBlue')
     
     is_roi_preview_activated_box = Checkbutton(self,text='is_roi_preview_activated',variable=is_roi_preview_activated,command=roi_configuration_preview_start_thread,background = 'SkyBlue')
     close_video_tip_label=Label(self,text='please press "q" to close the video',background = 'IndianRed')
     #set the layout
     interest_area_x_start_label.grid(row=0,column=0)
     interest_area_x_start_box.grid(row=0,column=1)
     interest_area_y_start_label.grid(row=0,column=2)
     interest_area_y_start_box.grid(row=0,column=3)
     
     interest_area_x_end_label.grid(row=1,column=0)
     interest_area_x_end_box.grid(row=1,column=1)
     interest_area_y_end_label.grid(row=1,column=2)
     interest_area_y_end_box.grid(row=1,column=3)  
    
     line_crossing_detection_pos_left_label.grid(row=2,column=0)
     line_crossing_detection_pos_left_box.grid(row=2,column=1)
     line_crossing_detection_pos_right_label.grid(row=2,column=2)
     line_crossing_detection_pos_right_box.grid(row=2,column=3)
     line_crossing_detection_pos_top_label.grid(row=3,column=0)
     line_crossing_detection_pos_top_box.grid(row=3,column=1)
     line_crossing_detection_pos_bottom_label.grid(row=3,column=2)
     line_crossing_detection_pos_bottom_box.grid(row=3,column=3)
     
     is_lane_first_available_box.grid(row=4,column=0)
     is_lane_second_available_box.grid(row=4,column=1)
     is_lane_third_available_box.grid(row=4,column=2)
     
     left_detection_position_lane_first_start_label.grid(row=5,column=0)
     left_detection_position_lane_first_start_box.grid(row=5,column=1)
     left_detection_position_lane_first_end_label.grid(row=5,column=2)
     left_detection_position_lane_first_end_box.grid(row=5,column=3)
     
     right_detection_position_lane_first_start_label.grid(row=6,column=0)
     right_detection_position_lane_first_start_box.grid(row=6,column=1)
     right_detection_position_lane_first_end_label.grid(row=6,column=2)
     right_detection_position_lane_first_end_box.grid(row=6,column=3)
     
     left_detection_position_lane_second_start_label.grid(row=7,column=0)
     left_detection_position_lane_second_start_box.grid(row=7,column=1)
     left_detection_position_lane_second_end_label.grid(row=7,column=2)
     left_detection_position_lane_second_end_box.grid(row=7,column=3)
     right_detection_position_lane_second_start_label.grid(row=8,column=0)
     right_detection_position_lane_second_start_box.grid(row=8,column=1)
     right_detection_position_lane_second_end_label.grid(row=8,column=2)
     right_detection_position_lane_second_end_box.grid(row=8,column=3)
     
     left_detection_position_lane_third_start_label.grid(row=9,column=0)
     left_detection_position_lane_third_start_box.grid(row=9,column=1)
     left_detection_position_lane_third_end_label.grid(row=9,column=2)
     left_detection_position_lane_third_end_box.grid(row=9,column=3)
     right_detection_position_lane_third_start_label.grid(row=10,column=0)
     right_detection_position_lane_third_start_box.grid(row=10,column=1)
     right_detection_position_lane_third_end_label.grid(row=10,column=2)
     right_detection_position_lane_third_end_box.grid(row=10,column=3)
     
     speed_detection_position_lane_top_label.grid(row=11,column=0)
     speed_detection_position_lane_top_box.grid(row=11,column=1)
     speed_detection_position_lane_bottom_label.grid(row=11,column=2)
     speed_detection_position_lane_bottom_box.grid(row=11,column=3)
     left_speed_detection_position_lane_first_label.grid(row=12,column=0)
     left_speed_detection_position_lane_first_box.grid(row=12,column=1)
     right_speed_detection_position_lane_first_label.grid(row=12,column=2)
     right_speed_detection_position_lane_first_box.grid(row=12,column=3)
     left_speed_detection_position_lane_second_label.grid(row=13,column=0)
     left_speed_detection_position_lane_second_box.grid(row=13,column=1)
     right_speed_detection_position_lane_second_label.grid(row=13,column=2)
     right_speed_detection_position_lane_second_box.grid(row=13,column=3)
     left_speed_detection_position_lane_third_label.grid(row=14,column=0)
     left_speed_detection_position_lane_third_box.grid(row=14,column=1)
     right_speed_detection_position_lane_third_label.grid(row=14,column=2)
     right_speed_detection_position_lane_third_box.grid(row=14,column=3)
     
     leave_speed_detection_position_lane_top_label.grid(row=15,column=0)
     leave_speed_detection_position_lane_top_box.grid(row=15,column=1)
     leave_speed_detection_position_lane_bottom_label.grid(row=15,column=2)
     leave_speed_detection_position_lane_bottom_box.grid(row=15,column=3)
      
     light_detected_color_label.grid(row=16,column=0)
     light_detected_color_box.grid(row=16,column=1)
     traffic_light_pos_top_label.grid(row=16,column=2)
     traffic_light_pos_top_box.grid(row=16,column=3)
     traffic_light_pos_bottom_label.grid(row=17,column=0)
     traffic_light_pos_bottom_box.grid(row=17,column=1)
     traffic_light_pos_left_label.grid(row=17,column=2)
     traffic_light_pos_left_box.grid(row=17,column=3)
     traffic_light_pos_right_label.grid(row=18,column=0)
     traffic_light_pos_right_box.grid(row=18,column=1)
     
     speed_limit_label_label.grid(row=18,column=2)
     speed_limit_label_box.grid(row=18,column=3)
     
     pixel_to_real_length_label.grid(row=19,column=0)
     pixel_to_real_length_box.grid(row=19,column=1)
     pixel_height_compensate_label.grid(row=19,column=2)
     pixel_height_compensate_box.grid(row=19,column=3)
      
     line_crossing_detection_interval_in_each_lane_label.grid(row=20,column=0)
     line_crossing_detection_interval_in_each_lane_box.grid(row=20,column=1)
     
     button_video_file_choose.grid(row=21,column=0)
     button_video_detection.grid(row=21,column=1)
     is_roi_preview_activated_box.grid(row=21,column=2)
     
     button_roi_configuration_load.grid(row=22,column=0)
     button_activate_database_ui.grid(row=22,column=1)
     button_roi_configuration_save.grid(row=22,column=2)
      
     close_video_tip_label.grid(row=23,column=1)
#     def get_file_name():
#         global VIDEO_FILE_PATH
#         global CURRENT_PATH
#         global VIDEO_FILE_NAME
#         video_files_path= CURRENT_PATH+'/videos'
#         VIDEO_FILE_PATH = tkinter.filedialog.askopenfilename(filetypes=[("All files", "*.mp4 *.avi")],initialdir=video_files_path)
#         default_file_name=(VIDEO_FILE_PATH.split('/')[-1]).split('.')[0]
#         VIDEO_FILE_NAME=default_file_name
#    print(VIDEO_FILE_PATH)

def get_file_name():
    global VIDEO_FILE_PATH
    global CURRENT_PATH
    global VIDEO_FILE_NAME
    video_files_path= CURRENT_PATH+'/videos'
    VIDEO_FILE_PATH = tkinter.filedialog.askopenfilename(filetypes=[("All files", "*.mp4 *.avi")],initialdir=video_files_path)
    default_file_name=(VIDEO_FILE_PATH.split('/')[-1]).split('.')[0]
    VIDEO_FILE_NAME=default_file_name
    print(VIDEO_FILE_PATH)

def save_roi_configuration():
    global roi_configuration_info
    
    global INTEREST_AREA_X_START
    global INTEREST_AREA_Y_START
    global INTEREST_AREA_X_END
    global INTEREST_AREA_Y_END
    global LINE_CROSSING_DETECTION_POS_LEFT
    global LINE_CROSSING_DETECTION_POS_RIGHT
    global LINE_CROSSING_DETECTION_POS_TOP
    global LINE_CROSSING_DETECTION_POS_BOTTOM
    global IS_LANE_FIRST_AVAILABLE
    global IS_LANE_SECOND_AVAILABLE
    global IS_LANE_THIRD_AVAILABLE
    global LEFT_DETECTION_POSITION_LANE_FIRST_START
    global LEFT_DETECTION_POSITION_LANE_FIRST_END
    global RIGHT_DETECTION_POSITION_LANE_FIRST_START
    global RIGHT_DETECTION_POSITION_LANE_FIRST_END
    global LEFT_DETECTION_POSITION_LANE_SECOND_START
    global LEFT_DETECTION_POSITION_LANE_SECOND_END
    global RIGHT_DETECTION_POSITION_LANE_SECOND_START
    global RIGHT_DETECTION_POSITION_LANE_SECOND_END
    global LEFT_DETECTION_POSITION_LANE_THIRD_START
    global LEFT_DETECTION_POSITION_LANE_THIRD_END
    global RIGHT_DETECTION_POSITION_LANE_THIRD_START
    global RIGHT_DETECTION_POSITION_LANE_THIRD_END
    global SPEED_DETECTION_POSITION_LANE_TOP
    global SPEED_DETECTION_POSITION_LANE_BOTTOM
    global LEFT_SPEED_DETECTION_POSITION_LANE_FIRST
    global RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST
    global LEFT_SPEED_DETECTION_POSITION_LANE_SECOND
    global RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND
    global LEFT_SPEED_DETECTION_POSITION_LANE_THIRD
    global RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD
    global LEAVE_SPEED_DETECTION_POSITION_LANE_TOP
    global LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM
    global SPEED_LIMIT
    global PIXEL_TO_REAL_LENGTH
    global PIXEL_HEIGHT_COMPENSATE
    global DETECTED_LIGHT_COLOR
    global TRAFFIC_LIGHT_POS_TOP
    global TRAFFIC_LIGHT_POS_BOTTOM
    global TRAFFIC_LIGHT_POS_LEFT
    global TRAFFIC_LIGHT_POS_RIGHT
    
    LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE=line_crossing_detection_interval_in_each_lane.get()

    INTEREST_AREA_X_START=interest_area_x_start.get()
    INTEREST_AREA_Y_START=interest_area_y_start.get()
    INTEREST_AREA_X_END=interest_area_x_end.get()
    INTEREST_AREA_Y_END=interest_area_y_end.get()
    
    LINE_CROSSING_DETECTION_POS_LEFT=line_crossing_detection_pos_left.get()
    LINE_CROSSING_DETECTION_POS_RIGHT=line_crossing_detection_pos_right.get()
    LINE_CROSSING_DETECTION_POS_TOP=line_crossing_detection_pos_top.get()
    LINE_CROSSING_DETECTION_POS_BOTTOM=line_crossing_detection_pos_bottom.get()
    
    IS_LANE_FIRST_AVAILABLE=is_lane_first_available.get()
    IS_LANE_SECOND_AVAILABLE=is_lane_second_available.get()
    IS_LANE_THIRD_AVAILABLE=is_lane_third_available.get()
    
    LEFT_DETECTION_POSITION_LANE_FIRST_START=left_detection_position_lane_first_start.get()
    LEFT_DETECTION_POSITION_LANE_FIRST_END=left_detection_position_lane_first_end.get()
    RIGHT_DETECTION_POSITION_LANE_FIRST_START=right_detection_position_lane_first_start.get()
    RIGHT_DETECTION_POSITION_LANE_FIRST_END=right_detection_position_lane_first_end.get()   
    LEFT_DETECTION_POSITION_LANE_SECOND_START=left_detection_position_lane_second_start.get()
    LEFT_DETECTION_POSITION_LANE_SECOND_END=left_detection_position_lane_second_end.get()
    RIGHT_DETECTION_POSITION_LANE_SECOND_START=right_detection_position_lane_second_start.get()
    RIGHT_DETECTION_POSITION_LANE_SECOND_END=right_detection_position_lane_second_end.get()
    LEFT_DETECTION_POSITION_LANE_THIRD_START=left_detection_position_lane_third_start.get()
    LEFT_DETECTION_POSITION_LANE_THIRD_END=left_detection_position_lane_third_end.get()
    RIGHT_DETECTION_POSITION_LANE_THIRD_START=right_detection_position_lane_third_start.get()
    RIGHT_DETECTION_POSITION_LANE_THIRD_END=right_detection_position_lane_third_end.get()
    
    SPEED_DETECTION_POSITION_LANE_TOP=speed_detection_position_lane_top.get()
    SPEED_DETECTION_POSITION_LANE_BOTTOM=speed_detection_position_lane_bottom.get()
    
    LEFT_SPEED_DETECTION_POSITION_LANE_FIRST=left_speed_detection_position_lane_first.get()
    RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST=right_speed_detection_position_lane_first.get()
    LEFT_SPEED_DETECTION_POSITION_LANE_SECOND=left_speed_detection_position_lane_second.get()
    RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND=right_speed_detection_position_lane_second.get()
    LEFT_SPEED_DETECTION_POSITION_LANE_THIRD=left_speed_detection_position_lane_third.get()
    RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD=right_speed_detection_position_lane_third.get()
    
    LEAVE_SPEED_DETECTION_POSITION_LANE_TOP=leave_speed_detection_position_lane_top.get()
    LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM=leave_speed_detection_position_lane_bottom.get()
    
    DETECTED_LIGHT_COLOR=light_detected_color.get()
    TRAFFIC_LIGHT_POS_TOP=traffic_light_pos_top.get()
    TRAFFIC_LIGHT_POS_BOTTOM=traffic_light_pos_bottom.get()
    TRAFFIC_LIGHT_POS_LEFT=traffic_light_pos_left.get()
    TRAFFIC_LIGHT_POS_RIGHT=traffic_light_pos_right.get()
    
    SPEED_LIMIT=speed_limit.get()
    PIXEL_TO_REAL_LENGTH=pixel_to_real_length.get()
    PIXEL_HEIGHT_COMPENSATE=pixel_height_compensate.get()
    
    LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE=line_crossing_detection_interval_in_each_lane.get()

    roi_configuration_info=str(INTEREST_AREA_X_START)+","+str(INTEREST_AREA_Y_START)+","+str(INTEREST_AREA_X_END)+","+str(INTEREST_AREA_Y_END)+","+\
    str(LINE_CROSSING_DETECTION_POS_LEFT)+","+str(LINE_CROSSING_DETECTION_POS_RIGHT)+","+str(LINE_CROSSING_DETECTION_POS_TOP)+","+str(LINE_CROSSING_DETECTION_POS_BOTTOM)+","+\
    str(IS_LANE_FIRST_AVAILABLE)+","+str(IS_LANE_SECOND_AVAILABLE)+","+str(IS_LANE_THIRD_AVAILABLE)+","+\
    str(LEFT_DETECTION_POSITION_LANE_FIRST_START)+","+str(LEFT_DETECTION_POSITION_LANE_FIRST_END)+","+\
    str(RIGHT_DETECTION_POSITION_LANE_FIRST_START)+","+str(RIGHT_DETECTION_POSITION_LANE_FIRST_END)+","+\
    str(LEFT_DETECTION_POSITION_LANE_SECOND_START)+","+str(LEFT_DETECTION_POSITION_LANE_SECOND_END)+","+\
    str(RIGHT_DETECTION_POSITION_LANE_SECOND_START)+","+str(RIGHT_DETECTION_POSITION_LANE_SECOND_END)+","+\
    str(LEFT_DETECTION_POSITION_LANE_THIRD_START)+","+str(LEFT_DETECTION_POSITION_LANE_THIRD_END)+","+\
    str(RIGHT_DETECTION_POSITION_LANE_THIRD_START)+","+str(RIGHT_DETECTION_POSITION_LANE_THIRD_END)+","+\
    str(SPEED_DETECTION_POSITION_LANE_TOP)+","+str(SPEED_DETECTION_POSITION_LANE_BOTTOM)+","+\
    str(LEFT_SPEED_DETECTION_POSITION_LANE_FIRST)+","+str(RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST)+","+\
    str(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND)+","+str(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND)+","+\
    str(LEFT_SPEED_DETECTION_POSITION_LANE_THIRD)+","+str(RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD)+","+\
    str(LEAVE_SPEED_DETECTION_POSITION_LANE_TOP)+","+str(LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM)+","+\
    str(DETECTED_LIGHT_COLOR)+","+str(TRAFFIC_LIGHT_POS_TOP)+","+str(TRAFFIC_LIGHT_POS_BOTTOM)+","+str(TRAFFIC_LIGHT_POS_LEFT)+","+str(TRAFFIC_LIGHT_POS_RIGHT)+","+\
    str(SPEED_LIMIT)+","+\
    str(PIXEL_TO_REAL_LENGTH)+","+str(PIXEL_HEIGHT_COMPENSATE)+","+\
    str(LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE)
    print('roi_configuration_info: '+roi_configuration_info)
    save_configuration_file(roi_configuration_info)

def load_roi_configuration():
    global VIDEO_FILE_PATH
    global CURRENT_PATH

    global INTEREST_AREA_X_START
    global INTEREST_AREA_Y_START
    global INTEREST_AREA_X_END
    global INTEREST_AREA_Y_END
    global LINE_CROSSING_DETECTION_POS_LEFT
    global LINE_CROSSING_DETECTION_POS_RIGHT
    global LINE_CROSSING_DETECTION_POS_TOP
    global LINE_CROSSING_DETECTION_POS_BOTTOM
    global IS_LANE_FIRST_AVAILABLE
    global IS_LANE_SECOND_AVAILABLE
    global IS_LANE_THIRD_AVAILABLE
    global LEFT_DETECTION_POSITION_LANE_FIRST_START
    global LEFT_DETECTION_POSITION_LANE_FIRST_END
    global RIGHT_DETECTION_POSITION_LANE_FIRST_START
    global RIGHT_DETECTION_POSITION_LANE_FIRST_END
    global LEFT_DETECTION_POSITION_LANE_SECOND_START
    global LEFT_DETECTION_POSITION_LANE_SECOND_END
    global RIGHT_DETECTION_POSITION_LANE_SECOND_START
    global RIGHT_DETECTION_POSITION_LANE_SECOND_END
    global LEFT_DETECTION_POSITION_LANE_THIRD_START
    global LEFT_DETECTION_POSITION_LANE_THIRD_END
    global RIGHT_DETECTION_POSITION_LANE_THIRD_START
    global RIGHT_DETECTION_POSITION_LANE_THIRD_END
    global SPEED_DETECTION_POSITION_LANE_TOP
    global SPEED_DETECTION_POSITION_LANE_BOTTOM
    global LEFT_SPEED_DETECTION_POSITION_LANE_FIRST
    global RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST
    global LEFT_SPEED_DETECTION_POSITION_LANE_SECOND
    global RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND
    global LEFT_SPEED_DETECTION_POSITION_LANE_THIRD
    global RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD
    global LEAVE_SPEED_DETECTION_POSITION_LANE_TOP
    global LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM
    global SPEED_LIMIT
    global PIXEL_TO_REAL_LENGTH
    global PIXEL_HEIGHT_COMPENSATE
    global DETECTED_LIGHT_COLOR
    global TRAFFIC_LIGHT_POS_TOP
    global TRAFFIC_LIGHT_POS_BOTTOM
    global TRAFFIC_LIGHT_POS_LEFT
    global TRAFFIC_LIGHT_POS_RIGHT
    global LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE
    roi_configuration_files_path= CURRENT_PATH+'/roi_configuration_files'
    default_file_name=(VIDEO_FILE_PATH.split('/')[-1]).split('.')[0]
    
    
    video_name = tkinter.filedialog.askopenfilename(filetypes=[('Text', '*.txt')],initialdir=roi_configuration_files_path,initialfile=default_file_name)
    f = open(video_name, 'r')
    roi_info=f.read()
    f.close()
    (INTEREST_AREA_X_START,INTEREST_AREA_Y_START,INTEREST_AREA_X_END,INTEREST_AREA_Y_END,
    LINE_CROSSING_DETECTION_POS_LEFT,LINE_CROSSING_DETECTION_POS_RIGHT,LINE_CROSSING_DETECTION_POS_TOP,LINE_CROSSING_DETECTION_POS_BOTTOM,
    IS_LANE_FIRST_AVAILABLE_NAME,IS_LANE_SECOND_AVAILABLE_NAME,IS_LANE_THIRD_AVAILABLE_NAME,
    LEFT_DETECTION_POSITION_LANE_FIRST_START,LEFT_DETECTION_POSITION_LANE_FIRST_END,
    RIGHT_DETECTION_POSITION_LANE_FIRST_START,RIGHT_DETECTION_POSITION_LANE_FIRST_END,
    LEFT_DETECTION_POSITION_LANE_SECOND_START,LEFT_DETECTION_POSITION_LANE_SECOND_END,
    RIGHT_DETECTION_POSITION_LANE_SECOND_START,RIGHT_DETECTION_POSITION_LANE_SECOND_END,
    LEFT_DETECTION_POSITION_LANE_THIRD_START,LEFT_DETECTION_POSITION_LANE_THIRD_END,
    RIGHT_DETECTION_POSITION_LANE_THIRD_START,RIGHT_DETECTION_POSITION_LANE_THIRD_END,
    SPEED_DETECTION_POSITION_LANE_TOP,SPEED_DETECTION_POSITION_LANE_BOTTOM,
    LEFT_SPEED_DETECTION_POSITION_LANE_FIRST,RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST,
    LEFT_SPEED_DETECTION_POSITION_LANE_SECOND,RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND,
    LEFT_SPEED_DETECTION_POSITION_LANE_THIRD,RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD,
    LEAVE_SPEED_DETECTION_POSITION_LANE_TOP,LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM,
    DETECTED_LIGHT_COLOR,TRAFFIC_LIGHT_POS_TOP,TRAFFIC_LIGHT_POS_BOTTOM,TRAFFIC_LIGHT_POS_LEFT,TRAFFIC_LIGHT_POS_RIGHT,
    SPEED_LIMIT,
    PIXEL_TO_REAL_LENGTH,PIXEL_HEIGHT_COMPENSATE,
    LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE)=roi_info.split(',')
    roi=roi_info.split(',')
    
    
    INTEREST_AREA_X_START=int(INTEREST_AREA_X_START)
    INTEREST_AREA_Y_START=int(INTEREST_AREA_Y_START)
    INTEREST_AREA_X_END=int(INTEREST_AREA_X_END)
    INTEREST_AREA_Y_END=int(INTEREST_AREA_Y_END)
    LINE_CROSSING_DETECTION_POS_LEFT=int(LINE_CROSSING_DETECTION_POS_LEFT)
    LINE_CROSSING_DETECTION_POS_RIGHT=int(LINE_CROSSING_DETECTION_POS_RIGHT)
    LINE_CROSSING_DETECTION_POS_TOP=int(LINE_CROSSING_DETECTION_POS_TOP)
    LINE_CROSSING_DETECTION_POS_BOTTOM=int(LINE_CROSSING_DETECTION_POS_BOTTOM)
    LEFT_DETECTION_POSITION_LANE_FIRST_START=int(LEFT_DETECTION_POSITION_LANE_FIRST_START)
    LEFT_DETECTION_POSITION_LANE_FIRST_END=int(LEFT_DETECTION_POSITION_LANE_FIRST_END)
    RIGHT_DETECTION_POSITION_LANE_FIRST_START=int(RIGHT_DETECTION_POSITION_LANE_FIRST_START)
    RIGHT_DETECTION_POSITION_LANE_FIRST_END=int(RIGHT_DETECTION_POSITION_LANE_FIRST_END)
    LEFT_DETECTION_POSITION_LANE_SECOND_START=int(LEFT_DETECTION_POSITION_LANE_SECOND_START)
    LEFT_DETECTION_POSITION_LANE_SECOND_END=int(LEFT_DETECTION_POSITION_LANE_SECOND_END)
    RIGHT_DETECTION_POSITION_LANE_SECOND_START=int(RIGHT_DETECTION_POSITION_LANE_SECOND_START)
    RIGHT_DETECTION_POSITION_LANE_SECOND_END=int(RIGHT_DETECTION_POSITION_LANE_SECOND_END)
    LEFT_DETECTION_POSITION_LANE_THIRD_START=int(LEFT_DETECTION_POSITION_LANE_THIRD_START)
    LEFT_DETECTION_POSITION_LANE_THIRD_END=int(LEFT_DETECTION_POSITION_LANE_THIRD_END)
    RIGHT_DETECTION_POSITION_LANE_THIRD_START=int(RIGHT_DETECTION_POSITION_LANE_THIRD_START)
    RIGHT_DETECTION_POSITION_LANE_THIRD_END=int(RIGHT_DETECTION_POSITION_LANE_THIRD_END)
    SPEED_DETECTION_POSITION_LANE_TOP=int(SPEED_DETECTION_POSITION_LANE_TOP)
    SPEED_DETECTION_POSITION_LANE_BOTTOM=int(SPEED_DETECTION_POSITION_LANE_BOTTOM)
    LEFT_SPEED_DETECTION_POSITION_LANE_FIRST=int(LEFT_SPEED_DETECTION_POSITION_LANE_FIRST)
    RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST=int(RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST)
    LEFT_SPEED_DETECTION_POSITION_LANE_SECOND=int(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND)
    RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND=int(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND)
    LEFT_SPEED_DETECTION_POSITION_LANE_THIRD=int(LEFT_SPEED_DETECTION_POSITION_LANE_THIRD)
    RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD=int(RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD)
    LEAVE_SPEED_DETECTION_POSITION_LANE_TOP=int(LEAVE_SPEED_DETECTION_POSITION_LANE_TOP)
    LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM=int(LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM)
    TRAFFIC_LIGHT_POS_TOP=int(TRAFFIC_LIGHT_POS_TOP)
    TRAFFIC_LIGHT_POS_BOTTOM=int(TRAFFIC_LIGHT_POS_BOTTOM)
    TRAFFIC_LIGHT_POS_LEFT=int(TRAFFIC_LIGHT_POS_LEFT)
    TRAFFIC_LIGHT_POS_RIGHT=int(TRAFFIC_LIGHT_POS_RIGHT)
    SPEED_LIMIT=int(SPEED_LIMIT)
    PIXEL_TO_REAL_LENGTH=float(PIXEL_TO_REAL_LENGTH)
    PIXEL_HEIGHT_COMPENSATE=float(PIXEL_HEIGHT_COMPENSATE)
    LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE=float(LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE)

    print(default_file_name,'roi info: ',roi)
    #set the new value 
    interest_area_x_start.set(INTEREST_AREA_X_START)
    interest_area_y_start.set(INTEREST_AREA_Y_START)
    interest_area_x_end.set(INTEREST_AREA_X_END)
    interest_area_y_end.set(INTEREST_AREA_Y_END)    
     
    line_crossing_detection_pos_left.set(LINE_CROSSING_DETECTION_POS_LEFT)
    line_crossing_detection_pos_right.set(LINE_CROSSING_DETECTION_POS_RIGHT)  
    line_crossing_detection_pos_top.set(LINE_CROSSING_DETECTION_POS_TOP)
    line_crossing_detection_pos_bottom.set(LINE_CROSSING_DETECTION_POS_BOTTOM)
     
    if(IS_LANE_FIRST_AVAILABLE_NAME=='True'):
        IS_LANE_FIRST_AVAILABLE=True
    else:
        IS_LANE_FIRST_AVAILABLE=False
        
    if(IS_LANE_SECOND_AVAILABLE_NAME=='True'):
        IS_LANE_SECOND_AVAILABLE=True
    else:
        IS_LANE_SECOND_AVAILABLE=False
        
    if(IS_LANE_THIRD_AVAILABLE_NAME=='True'):
        IS_LANE_THIRD_AVAILABLE=True
    else:
        IS_LANE_THIRD_AVAILABLE=False
        
    is_lane_first_available.set(IS_LANE_FIRST_AVAILABLE)
    is_lane_second_available.set(IS_LANE_SECOND_AVAILABLE)
    is_lane_third_available.set(IS_LANE_THIRD_AVAILABLE)
     
    left_detection_position_lane_first_start.set(LEFT_DETECTION_POSITION_LANE_FIRST_START)
    left_detection_position_lane_first_end.set(LEFT_DETECTION_POSITION_LANE_FIRST_END)
    right_detection_position_lane_first_start.set(RIGHT_DETECTION_POSITION_LANE_FIRST_START)
    right_detection_position_lane_first_end.set(RIGHT_DETECTION_POSITION_LANE_FIRST_END)

    left_detection_position_lane_second_start.set(LEFT_DETECTION_POSITION_LANE_SECOND_START)
    left_detection_position_lane_second_end.set(LEFT_DETECTION_POSITION_LANE_SECOND_END)
    right_detection_position_lane_second_start.set(RIGHT_DETECTION_POSITION_LANE_SECOND_START)
    right_detection_position_lane_second_end.set(RIGHT_DETECTION_POSITION_LANE_SECOND_END)
     
    left_detection_position_lane_third_start.set(LEFT_DETECTION_POSITION_LANE_THIRD_START)
    left_detection_position_lane_third_end.set(LEFT_DETECTION_POSITION_LANE_THIRD_END)
    right_detection_position_lane_third_start.set(RIGHT_DETECTION_POSITION_LANE_THIRD_START)
    right_detection_position_lane_third_end.set(RIGHT_DETECTION_POSITION_LANE_THIRD_END)
     
     
    speed_detection_position_lane_top.set(SPEED_DETECTION_POSITION_LANE_TOP)
    speed_detection_position_lane_bottom.set(SPEED_DETECTION_POSITION_LANE_BOTTOM)  
    left_speed_detection_position_lane_first.set(LEFT_SPEED_DETECTION_POSITION_LANE_FIRST)
    right_speed_detection_position_lane_first.set(RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST)
    left_speed_detection_position_lane_second.set(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND)
    right_speed_detection_position_lane_second.set(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND)
    left_speed_detection_position_lane_third.set(LEFT_SPEED_DETECTION_POSITION_LANE_THIRD)
    right_speed_detection_position_lane_third.set(RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD)
     
    leave_speed_detection_position_lane_top.set(LEAVE_SPEED_DETECTION_POSITION_LANE_TOP)
    leave_speed_detection_position_lane_bottom.set(LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM)
     
    speed_limit.set(SPEED_LIMIT)
     
    pixel_to_real_length.set(PIXEL_TO_REAL_LENGTH)
    pixel_height_compensate.set(PIXEL_HEIGHT_COMPENSATE)
     
    light_detected_color.set(DETECTED_LIGHT_COLOR)
    traffic_light_pos_top.set(TRAFFIC_LIGHT_POS_TOP)
    traffic_light_pos_bottom.set(TRAFFIC_LIGHT_POS_BOTTOM)
    traffic_light_pos_left.set(TRAFFIC_LIGHT_POS_LEFT)
    traffic_light_pos_right.set(TRAFFIC_LIGHT_POS_RIGHT)     
     
    line_crossing_detection_interval_in_each_lane.set(LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE)    
    
def save_configuration_file(roi_info):
    global VIDEO_FILE_PATH
    global CURRENT_PATH
    roi_configuration_files_path= CURRENT_PATH+'/roi_configuration_files'
    roi_configuration_info=roi_info
    default_file_name=(VIDEO_FILE_PATH.split('/')[-1]).split('.')[0]
    _filetypes = [
        ('Text', '*.txt'),
            ('All files', '*'),
            ]
    filename = tkinter.filedialog.asksaveasfilename(defaultextension='.txt',initialdir=roi_configuration_files_path,initialfile=default_file_name,filetypes = _filetypes)
    f = open(filename, 'w')
    f.write(roi_configuration_info)
    f.close()
    tkinter.messagebox.showinfo('ROI_SAVE_STATUS', 'File Is Saved Successfully.')

def roi_configuration_preview_start_thread():
    thread=threading.Thread(target=roi_configuration_preview,args=())
    thread.start()

def draw_roi_preview(frame):
    input_frame=frame
    text_offset_y=10
    cv2.rectangle(input_frame,(interest_area_x_start.get(),interest_area_y_start.get()),(interest_area_x_end.get(),interest_area_y_end.get()),(0,255,255),3)
    cv2.putText(input_frame,'region of interest',(interest_area_x_start.get(),interest_area_y_start.get()-text_offset_y),1,cv2.FONT_HERSHEY_COMPLEX,(0, 255, 255),2)
    
    cv2.rectangle(input_frame,(traffic_light_pos_left.get(),traffic_light_pos_top.get()),(traffic_light_pos_right.get(),traffic_light_pos_bottom.get()),(0, 255, 0),2)
    cv2.putText(input_frame,'traffic light color detection area',(traffic_light_pos_left.get(),traffic_light_pos_top.get()-text_offset_y),1,cv2.FONT_HERSHEY_COMPLEX,(0, 255, 0),2)
    
    if(is_lane_first_available.get()==True):
        cv2.putText(input_frame,'line crossing detection area',(left_detection_position_lane_first_start.get(),line_crossing_detection_pos_top.get()-text_offset_y),1,cv2.FONT_HERSHEY_COMPLEX,(0, 240, 0),2)
        
        cv2.line(input_frame,(left_detection_position_lane_first_start.get(),speed_detection_position_lane_top.get()),(left_detection_position_lane_first_end.get(),speed_detection_position_lane_top.get()+LINE_BOTTOM_HEIGHT),(0,240,0),4)
        cv2.line(input_frame,(right_detection_position_lane_first_start.get(),speed_detection_position_lane_top.get()),(right_detection_position_lane_first_end.get(),speed_detection_position_lane_top.get()+LINE_BOTTOM_HEIGHT),(0,255,0),4)    
                
        cv2.putText(input_frame,'vehicle detection area',(left_speed_detection_position_lane_first.get(),speed_detection_position_lane_top.get()-text_offset_y),1,cv2.FONT_HERSHEY_COMPLEX,(18, 74, 115),2)      
        cv2.rectangle(input_frame,(left_speed_detection_position_lane_first.get(),speed_detection_position_lane_top.get()),(right_speed_detection_position_lane_first.get(),speed_detection_position_lane_bottom.get()),(18, 74, 115),3)               
        
        cv2.putText(input_frame,'leave detection area',(left_speed_detection_position_lane_first.get(),leave_speed_detection_position_lane_top.get()-text_offset_y),1,cv2.FONT_HERSHEY_COMPLEX,(0, 0, 200),2)
        cv2.rectangle(input_frame,(left_speed_detection_position_lane_first.get(),leave_speed_detection_position_lane_top.get()),(right_speed_detection_position_lane_first.get(),leave_speed_detection_position_lane_bottom.get()),(0, 0, 200),2)
    if(is_lane_second_available.get()==True):
        cv2.line(input_frame,(left_detection_position_lane_second_start.get(),speed_detection_position_lane_top.get()),(left_detection_position_lane_second_end.get(),speed_detection_position_lane_top.get()+LINE_BOTTOM_HEIGHT),(0,240,0),4)
        cv2.line(input_frame,(right_detection_position_lane_second_start.get(),speed_detection_position_lane_top.get()),(right_detection_position_lane_second_end.get(),speed_detection_position_lane_top.get()+LINE_BOTTOM_HEIGHT),(0,255,0),4)                    

        cv2.rectangle(input_frame,(left_speed_detection_position_lane_second.get(),speed_detection_position_lane_top.get()),(right_speed_detection_position_lane_second.get(),speed_detection_position_lane_bottom.get()),(18, 74, 115),3)                   
        cv2.rectangle(input_frame,(left_speed_detection_position_lane_second.get(),leave_speed_detection_position_lane_top.get()),(right_speed_detection_position_lane_second.get(),leave_speed_detection_position_lane_bottom.get()),(0, 0, 200),2)
    if(is_lane_third_available.get()==True):
        cv2.line(input_frame,(left_detection_position_lane_third_start.get(),speed_detection_position_lane_top.get()),(left_detection_position_lane_third_end.get(),speed_detection_position_lane_top.get()+LINE_BOTTOM_HEIGHT),(0,240,0),4)
        cv2.line(input_frame,(right_detection_position_lane_third_start.get(),speed_detection_position_lane_top.get()),(right_detection_position_lane_third_end.get(),speed_detection_position_lane_top.get()+LINE_BOTTOM_HEIGHT),(0,255,0),4)                    

        cv2.rectangle(input_frame,(left_speed_detection_position_lane_third.get(),speed_detection_position_lane_top.get()),(right_speed_detection_position_lane_third.get(),speed_detection_position_lane_bottom.get()),(18, 74, 115),3)                   
        cv2.rectangle(input_frame,(left_speed_detection_position_lane_third.get(),leave_speed_detection_position_lane_top.get()),(right_speed_detection_position_lane_third.get(),leave_speed_detection_position_lane_bottom.get()),(0, 0, 200),2)
    cv2.rectangle(input_frame,(line_crossing_detection_pos_left.get(),line_crossing_detection_pos_top.get()),(line_crossing_detection_pos_right.get(),line_crossing_detection_pos_bottom.get()),(0,255,0),3)    
#this function is still need to be improved,should press q to quit the video preview,or the system may crash....
def roi_configuration_preview():
    is_preview_activated=is_roi_preview_activated.get()
    cap = cv2.VideoCapture(VIDEO_FILE_PATH)
    cv2.namedWindow('roi_preview',cv2.WINDOW_NORMAL)
    (ret, frame) = cap.read()
    while is_preview_activated==True:
        new_frame=frame.copy()
        draw_roi_preview(new_frame)
        cv2.imshow('roi_preview',new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_roi_preview_activated.set('False')
            break
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width,
            3)).astype(np.uint8)
def draw_roi(input_frame,counter):
    global TOTAL_PASSED_VEHICLE_COUNT
    
    input_frame=input_frame
    #these two variables are only used to draw roi,not for detection 
    DETECTION_LINE_HEIGHT=SPEED_DETECTION_POSITION_LANE_TOP
    DETECTION_LINE_HEIGHT_END=DETECTION_LINE_HEIGHT+300
    #traffic light area
    cv2.rectangle(input_frame,(TRAFFIC_LIGHT_POS_LEFT,TRAFFIC_LIGHT_POS_TOP),(TRAFFIC_LIGHT_POS_RIGHT,TRAFFIC_LIGHT_POS_BOTTOM),(0, 0, 255),2)
    #draw interest area
    cv2.rectangle((input_frame),(INTEREST_AREA_X_START,INTEREST_AREA_Y_START),(INTEREST_AREA_X_END,INTEREST_AREA_Y_END),(0,255,255),3)
                
               
    #draw roi of lane first
    if(IS_LANE_FIRST_AVAILABLE):
        cv2.line(input_frame,(LEFT_DETECTION_POSITION_LANE_FIRST_START,DETECTION_LINE_HEIGHT),(LEFT_DETECTION_POSITION_LANE_FIRST_END,DETECTION_LINE_HEIGHT_END),(0,240,0),4)
        cv2.line(input_frame,(RIGHT_DETECTION_POSITION_LANE_FIRST_START,DETECTION_LINE_HEIGHT),(RIGHT_DETECTION_POSITION_LANE_FIRST_END,DETECTION_LINE_HEIGHT_END),(0,255,0),4)                    
        #draw roi of first lane speed detection 'Brown'
        cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_FIRST,SPEED_DETECTION_POSITION_LANE_TOP),(RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST,SPEED_DETECTION_POSITION_LANE_BOTTOM),(18, 74, 115),3)                   
        #draw roi of first lane leave detection 'Red'
        cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_FIRST,LEAVE_SPEED_DETECTION_POSITION_LANE_TOP),(RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST,LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM),(0, 0, 200),2)
        #draw roi of lane second
    if(IS_LANE_SECOND_AVAILABLE):
        cv2.line(input_frame,(LEFT_DETECTION_POSITION_LANE_SECOND_START,DETECTION_LINE_HEIGHT),(LEFT_DETECTION_POSITION_LANE_SECOND_END,DETECTION_LINE_HEIGHT_END),(0,255,0),4)
        cv2.line(input_frame,(RIGHT_DETECTION_POSITION_LANE_SECOND_START,DETECTION_LINE_HEIGHT),(RIGHT_DETECTION_POSITION_LANE_SECOND_END,DETECTION_LINE_HEIGHT_END),(0,255,0),4)
        #draw roi of second lane speed detection Brown
        cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND,SPEED_DETECTION_POSITION_LANE_TOP),(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND,SPEED_DETECTION_POSITION_LANE_BOTTOM),(18, 74, 115),3)
        #cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND,SPEED_DETECTION_POSITION_LANE_TOP-80),(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND,SPEED_DETECTION_POSITION_LANE_BOTTOM),(0, 144, 144),5)
        #draw roi of second lane leave detection 'Red'
        cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_SECOND,LEAVE_SPEED_DETECTION_POSITION_LANE_TOP),(RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND,LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM),(0, 0, 200),2)
                    
    if(IS_LANE_THIRD_AVAILABLE):
        cv2.line(input_frame,(LEFT_DETECTION_POSITION_LANE_THIRD_START,DETECTION_LINE_HEIGHT),(LEFT_DETECTION_POSITION_LANE_THIRD_END,DETECTION_LINE_HEIGHT_END),(0,255,0),4)
        cv2.line(input_frame,(RIGHT_DETECTION_POSITION_LANE_THIRD_START,DETECTION_LINE_HEIGHT),(RIGHT_DETECTION_POSITION_LANE_THIRD_END,DETECTION_LINE_HEIGHT_END),(0,255,0),4)
        #draw roi of third lane speed detection Brown
        cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_THIRD,SPEED_DETECTION_POSITION_LANE_TOP),(RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD,SPEED_DETECTION_POSITION_LANE_BOTTOM),(18, 74, 115),3)
        #draw roi of third third leave detection 'Red'
        cv2.rectangle(input_frame,(LEFT_SPEED_DETECTION_POSITION_LANE_THIRD,LEAVE_SPEED_DETECTION_POSITION_LANE_TOP),(RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD,LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM),(0, 0, 200),2)
        #draw the roi of lane-transgressing detection and when the vehicle cross the line it will turn red.
    if counter == 1:
        cv2.rectangle(input_frame,(LINE_CROSSING_DETECTION_POS_LEFT,LINE_CROSSING_DETECTION_POS_TOP),(LINE_CROSSING_DETECTION_POS_RIGHT,LINE_CROSSING_DETECTION_POS_BOTTOM),(0,0,220),3)
    else:
        cv2.rectangle(input_frame,(LINE_CROSSING_DETECTION_POS_LEFT,LINE_CROSSING_DETECTION_POS_TOP),(LINE_CROSSING_DETECTION_POS_RIGHT,LINE_CROSSING_DETECTION_POS_BOTTOM),(0,255,0),3)
    
    TOTAL_PASSED_VEHICLE_COUNT=TOTAL_PASSED_VEHICLE_COUNT+counter

    cv2.putText(
            input_frame,
            'total_vehicle_count: ' + str(TOTAL_PASSED_VEHICLE_COUNT),
            (10, 40),
            font,
            2,
            (0, 235, 140),
            5,
            cv2.FONT_HERSHEY_SIMPLEX,
            )
# Download Model
# uncomment if you have not download the model yet
# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Loading label map
# Label maps map indices to category names, so that when our convolution network predicts 5, we know that this corresponds to airplane. Here I use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
        
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map,
        max_num_classes=NUM_CLASSES, use_display_name=True)

category_index = label_map_util.create_category_index(categories)

def reset_vehicle_count():
    global TOTAL_PASSED_VEHICLE_COUNT
    TOTAL_PASSED_VEHICLE_COUNT=0
# Detection
def object_detection_function():
    cap = cv2.VideoCapture(VIDEO_FILE_PATH)
    
    
    vis_util.set_detection_area_value(INTEREST_AREA_Y_START,INTEREST_AREA_Y_END,SPEED_LIMIT,VIDEO_FILE_NAME)
    reset_vehicle_count()
    image_saver.reset_stored_value()
    vehicle_detection_api.reset_stored_value()
    vehicle_detection_api.set_roi_value(LINE_CROSSING_DETECTION_POS_TOP,LINE_CROSSING_DETECTION_POS_BOTTOM,
                       IS_LANE_FIRST_AVAILABLE,IS_LANE_SECOND_AVAILABLE,IS_LANE_THIRD_AVAILABLE,
                       LEFT_DETECTION_POSITION_LANE_FIRST_START,RIGHT_DETECTION_POSITION_LANE_FIRST_START,
                       LEFT_DETECTION_POSITION_LANE_SECOND_START,RIGHT_DETECTION_POSITION_LANE_SECOND_START,
                       LEFT_DETECTION_POSITION_LANE_THIRD_START,RIGHT_DETECTION_POSITION_LANE_THIRD_START,
                       SPEED_DETECTION_POSITION_LANE_TOP,SPEED_DETECTION_POSITION_LANE_BOTTOM,
                       LEFT_SPEED_DETECTION_POSITION_LANE_FIRST,RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST,
                       LEFT_SPEED_DETECTION_POSITION_LANE_SECOND,RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND,
                       LEFT_SPEED_DETECTION_POSITION_LANE_THIRD,RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD,
                       LEAVE_SPEED_DETECTION_POSITION_LANE_TOP,LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM,
                       LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE,PIXEL_TO_REAL_LENGTH,PIXEL_HEIGHT_COMPENSATE,
                       DETECTED_LIGHT_COLOR,SPEED_LIMIT,LEFT_DETECTION_POSITION_LANE_FIRST_END)

    with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
    
                # Definite input and output Tensors for detection_graph
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                
    
                # for all the frames that are extracted from input video
                while cap.isOpened():
                    (ret, frame) = cap.read()
    
                    if not ret:
                        print ('end of the video file...')
                        break
    
                    input_frame = frame
                    #the start point(x,y) of interest area
                    #detect the vehicle in certain area to enhance performance
                    #starty:endy,startx:endx 
                    traffic_light_area_img=frame[TRAFFIC_LIGHT_POS_TOP+OFFSET:TRAFFIC_LIGHT_POS_BOTTOM-OFFSET,TRAFFIC_LIGHT_POS_LEFT+OFFSET:TRAFFIC_LIGHT_POS_RIGHT-OFFSET]
                    #get the color of traffic light and pass the color to detection
                    predicted_color = color_recognition_api.color_recognition(traffic_light_area_img)    

                    vehicle_detection_api.set_current_light_color(predicted_color)
    
                    interest_area=frame[INTEREST_AREA_Y_START:INTEREST_AREA_Y_END,INTEREST_AREA_X_START:INTEREST_AREA_X_END]
                   
                    #[1, None, None, 3]
                    image_np_expanded = np.expand_dims(interest_area, axis=0)
    
                    # Actual detection.
                    
                    (boxes, scores, classes, num) = \
                        sess.run([detection_boxes, detection_scores,
                                 detection_classes, num_detections],
                                 feed_dict={image_tensor: image_np_expanded})
    
                    # Visualization of the results of a detection.
                    (counter, csv_line) = \
                        vis_util.visualize_boxes_and_labels_on_image_array(
                        cap.get(1),
                        input_frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=2,
                        skip_scores=True,
                        interest_area_xpos_start=INTEREST_AREA_X_START,
                        interest_area_ypos_start=INTEREST_AREA_Y_START,
                        interest_area_xpos_end=INTEREST_AREA_X_END,
                        interest_area_ypos_end=INTEREST_AREA_Y_END
                        )
                    #draw roi on the video 
                    draw_roi(input_frame,counter)
    
                    cv2.namedWindow('vehicle detection',cv2.WINDOW_NORMAL)
                    cv2.imshow('vehicle detection', input_frame)
    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    
                cap.release()
                cv2.destroyAllWindows()
class DatabaseUI(tk.Toplevel):
  db_vehicle_name = 'vehicle_database.db'
  path=os.getcwd()+'/database_detected_vehicles_images'
  def __init__(self):
    super().__init__()
    self.title('Database UI')
    self.setup_UI()
  def run_query(self, query, parameters =()):
        with sqlite3.connect (self.db_vehicle_name) as conn:
            cursor = conn.cursor()
            query_result=cursor.execute(query, parameters)
            conn.commit()
        return query_result    
  def search_pattern(self,input_pattern):
        pattern=input_pattern
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)        
        query="SELECT * FROM vehicles_info WHERE vehicle_name LIKE ?"
        parmeters=('%'+pattern+'%',)
        db_rows=self.run_query(query,parmeters)
        for row in db_rows:
            self.tree.insert('',0, text = row[0], values = [row[1],row[2],row[3]])
        records=self.tree.get_children() 
        for element in records:
            self.tree.bind("<Double-Button-1>", self.on_record_clicked) 
  def serach_overspeed_record(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)        
        query='SELECT * FROM vehicles_info WHERE is_overspeed==1'
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0, text = row[0], values = [row[1],row[2],row[3]])
        records=self.tree.get_children()
        for element in records:
            self.tree.bind("<Double-Button-1>", self.on_record_clicked) 
  def serach_line_crossing_record(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)        
        query='SELECT * FROM vehicles_info WHERE is_line_crossing==1'
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0, text = row[0], values = [row[1],row[2],row[3]])
        records=self.tree.get_children()
        for element in records:
            self.tree.bind("<Double-Button-1>", self.on_record_clicked) 
  def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query= 'SELECT * FROM vehicles_info ORDER BY vehicle_name DESC'
        db_rows=self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0, text = row[0], values = [row[1],row[2],row[3]])
        records=self.tree.get_children()
        for element in records:
            self.tree.bind("<Double-Button-1>", self.on_record_clicked)
  def on_record_clicked(self,event):
        current_values=self.tree.item(self.tree.selection())['values'][0]
        file_info=current_values.split('_')
        vehicle_name=file_info[1]
        image_path=self.path+'/'+current_values+'.png'
        image = PIL.Image.open(image_path)
        image = image.resize((700, 500), PIL.Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = Label(self,image=photo)
        label.image = photo # keep a reference!
        label.grid(row=6,column=0,rowspan=5)
  def deleting(self):
        vehicle_name = self.tree.item(self.tree.selection())['values'][0]
        query='DELETE FROM vehicles_info WHERE vehicle_name= ?'
        self.run_query(query,(vehicle_name,))
        image_path=self.path+'/'+vehicle_name+'.png'
        os.remove(image_path)
        print(image_path,' has been deleted')
        self.viewing_records()   
  def setup_UI(self):
    tree_frame=tk.Frame(self)
    tree_frame.grid(row=0,column=0)
    self.tree = ttk.Treeview (tree_frame,height=7,columns=('col1','col2','col3'))
    self.tree.grid(row=2, column=0, columnspan=3)
    self.tree.heading('#0',text = 'id', anchor=W)
    self.tree.heading('col1',text = 'name', anchor=W)
    self.tree.heading('col2', text='line_crossing', anchor=W)
    self.tree.heading('col3', text='overspeed', anchor=W)
    
    bottom_frame=tk.Frame(self)
    bottom_frame.grid(row=3,column=0)

    ttk.Button(bottom_frame,text= 'Delete record',command=self.deleting).grid (row=0, column=0)
    ttk.Button(bottom_frame,text= 'Refresh',command=self.viewing_records).grid(row=0, column=1) 
    ttk.Button(bottom_frame, text='Search by pattern',command=lambda:self.search_pattern(pattern_name.get())).grid (row=0,column=2)  
    pattern_name = Entry(bottom_frame)
    pattern_name.grid(row=0, column =3)
    ttk.Button(bottom_frame,text= 'Search overspeed record',command=self.serach_overspeed_record).grid(row=1, column=0)
    ttk.Button(bottom_frame,text= 'Search line crossing record',command=self.serach_line_crossing_record).grid(row=1, column=2)
    
    self.viewing_records()
         

if __name__ == '__main__':
  app = MainWindow()
  app.mainloop()