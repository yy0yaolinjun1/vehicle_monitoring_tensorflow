#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils.image_utils import image_saver


is_doubled_solid_line_detection_in_interval=False
last_detected_frame_of_doubled_solid_line_detection=0
is_doubled_solid_line_crossing_detected=[0]
WIDTH_OF_TURNING_VEHICLE=500

is_vehicle_detected = [0]

is_vehicle_detected_lane_first_in_interval=False
last_detected_frame_in_lane_first=0
is_vehicle_detected_lane_second_in_interval=False
last_detected_frame_in_lane_second=0
is_vehicle_detected_lane_third_in_interval=False
last_detected_frame_in_lane_third=0

is_in_lane_first=False # to detect whether the vehicle has leaved in first lane
is_in_lane_second=False
is_in_lane_third=False
is_in_leave_lane_second=False

current_frame_number_lane_first_list = [0]
current_frame_number_lane_second_list = [0]
current_frame_number_lane_third_list = [0]

bottom_position_of_detected_vehicle = [0]

IS_LANE_FIRST_AVAILABLE=True
IS_LANE_SECOND_AVAILABLE=True
IS_LANE_THIRD_AVAILABLE=False

last_frame_bottom_position_of_detected_vehicle_in_lane_first=[0]
last_frame_bottom_position_of_detected_vehicle_in_lane_second=[0]
last_frame_bottom_position_of_detected_vehicle_in_lane_third=[0]

ROI_TOP_POSITION=0
ROI_BOTTOM_POSSTION=0

#The interval for vehicle detection,as the width of ROI is ROI_BOTTOM_POSSTION-ROI_TOP_POSSTION
#Therefore,a vehicle may be detected for more than 1 time.
LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE=0
#pos of line_crosssing detection
LINE_CROSSING_DETECTION_POS_TOP=0
LINE_CROSSING_DETECTION_POS_BOTTOM=0

LEFT_DETECTION_POSITION_LANE_FIRST=0
RIGHT_DETECTION_POSITION_LANE_FIRST=0

LEFT_DETECTION_POSITION_LANE_SECOND=0
RIGHT_DETECTION_POSITION_LANE_SECOND=0

LEFT_DETECTION_POSITION_LANE_THIRD=0
RIGHT_DETECTION_POSITION_LANE_THIRD=0
#pos of speed detection
SPEED_DETECTION_POSITION_LANE_TOP=0
SPEED_DETECTION_POSITION_LANE_BOTTOM=0

LEFT_SPEED_DETECTION_POSITION_LANE_FIRST=0
RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST=0

LEFT_SPEED_DETECTION_POSITION_LANE_SECOND=0
RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND=0

LEFT_SPEED_DETECTION_POSITION_LANE_THIRD=0
RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD=0
#vehicle leave detection in each lane
LEAVE_SPEED_DETECTION_POSITION_LANE_TOP=0
LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM=0

PIXEL_TO_REAL_LENGTH=0 #(suppose 1pixel~=0.02m)
PIXEL_HEIGHT_COMPENSATE=0 #per pixel increase 0.0002 perspective projection,with vehicle moving forward,the distance 1pixel = higher distance

DETECTED_LIGHT_COLOR=''
is_running_red_line=False
current_light_color=''

is_overspeed_detection_in_lane_first_in_interval=False
is_overspeed_detection_in_lane_second_in_interval=False
is_overspeed_detection_in_lane_third_in_interval=False

is_converse_crossing_in_lane_first_in_interval=False
is_converse_crossing_in_lane_second_in_interval=False
is_converse_crossing_in_lane_third_in_interval=False
detected_pixel_length_of_converse_crossing_in_lane_first=[0]
detected_pixel_length_of_converse_crossing_in_lane_second=[0]
detected_pixel_length_of_converse_crossing_in_lane_third=[0]
last_detected_frame_of_converse_crossing_in_lane_first=[0]
last_detected_frame_of_converse_crossing_in_lane_second=[0]
last_detected_frame_of_converse_crossing_in_lane_third=[0]

is_converse_running=False

SPEED_LIMIT=0
FPS=25 #the fps depends on the video
#when run the new video,the valued should be reset
def reset_stored_value():
    global is_vehicle_detected
    global is_vehicle_detected_lane_first_in_interval
    global last_detected_frame_in_lane_first
    global is_vehicle_detected_lane_second_in_interval
    global last_detected_frame_in_lane_second
    global is_vehicle_detected_lane_third_in_interval
    global last_detected_frame_in_lane_third
    global current_frame_number_lane_first_list
    global current_frame_number_lane_second_list
    global current_frame_number_lane_third_list
    global last_frame_bottom_position_of_detected_vehicle_in_lane_first
    global last_frame_bottom_position_of_detected_vehicle_in_lane_second
    global last_frame_bottom_position_of_detected_vehicle_in_lane_third
    global is_running_red_line
    global is_overspeed_detection_in_lane_first_in_interval
    global is_overspeed_detection_in_lane_second_in_interval
    global is_overspeed_detection_in_lane_third_in_interval
    global last_detected_overspeed_frame_in_speed_detection_area_first
    global last_detected_overspeed_frame_in_speed_detection_area_second
    global last_detected_overspeed_frame_in_speed_detection_area_third
    global is_doubled_solid_line_detection_in_interval
    global last_detected_frame_of_doubled_solid_line_detection
    global is_doubled_solid_line_crossing_detected
    
    global is_converse_crossing_in_lane_first_in_interval
    global is_converse_crossing_in_lane_second_in_interval
    global is_converse_crossing_in_lane_third_in_interval
    global detected_pixel_length_of_converse_crossing_in_lane_first
    global detected_pixel_length_of_converse_crossing_in_lane_second
    global detected_pixel_length_of_converse_crossing_in_lane_third
    global last_detected_frame_of_converse_crossing_in_lane_first
    global last_detected_frame_of_converse_crossing_in_lane_second
    global last_detected_frame_of_converse_crossing_in_lane_third
    
    
    is_vehicle_detected = [0]
    is_vehicle_detected_lane_first_in_interval=False
    last_detected_frame_in_lane_first=0
    is_vehicle_detected_lane_second_in_interval=False
    last_detected_frame_in_lane_second=0
    is_vehicle_detected_lane_third_in_interval=False
    last_detected_frame_in_lane_third=0
    
    current_frame_number_lane_first_list = [0]
    current_frame_number_lane_second_list = [0]
    current_frame_number_lane_third_list = [0]
    
    last_frame_bottom_position_of_detected_vehicle_in_lane_first=[0]
    last_frame_bottom_position_of_detected_vehicle_in_lane_second=[0]
    last_frame_bottom_position_of_detected_vehicle_in_lane_third=[0]
    
    
    is_running_red_line=False
    
    is_overspeed_detection_in_lane_first_in_interval=False
    is_overspeed_detection_in_lane_second_in_interval=False
    is_overspeed_detection_in_lane_third_in_interval=False
    last_detected_overspeed_frame_in_speed_detection_area_first=[0]
    last_detected_overspeed_frame_in_speed_detection_area_second=[0]
    last_detected_overspeed_frame_in_speed_detection_area_third=[0]
    
    is_doubled_solid_line_detection_in_interval=False
    last_detected_frame_of_doubled_solid_line_detection=0
    is_doubled_solid_line_crossing_detected=[0]
    
    is_converse_crossing_in_lane_first_in_interval=False
    is_converse_crossing_in_lane_second_in_interval=False
    is_converse_crossing_in_lane_third_in_interval=False
    detected_pixel_length_of_converse_crossing_in_lane_first=[0]
    detected_pixel_length_of_converse_crossing_in_lane_second=[0]
    detected_pixel_length_of_converse_crossing_in_lane_third=[0]
    last_detected_frame_of_converse_crossing_in_lane_first=[0]
    last_detected_frame_of_converse_crossing_in_lane_second=[0]
    last_detected_frame_of_converse_crossing_in_lane_third=[0]
    
def set_roi_value(line_crossing_detection_pos_top=0,line_crossing_detection_pos_bottom=0,
                  is_lane_first_available=True,is_lane_second_available=True,is_lane_third_available=True,
                  left_detection_pos_first_start=0,right_detection_pos_first_end=0,
                  left_detection_pos_second_start=0,right_detection_pos_second_end=0,
                  left_detection_pos_third_start=0,right_detection_pos_third_end=0,
                  speed_detection_pos_lane_top=0,speed_detection_pos_lane_bottom=0,
                  left_speed_detection_pos_lane_first=0,right_speed_detection_pos_lane_first=0,
                  left_speed_detection_pos_lane_second=0,right_speed_detection_pos_lane_second=0,
                  left_speed_detection_pos_lane_third=0,right_speed_detection_pos_lane_third=0,
                  leave_speed_detection_position_lane_top=0,leave_speed_detection_position_lane_bottom=0,
                  line_crossing_detection_interval_in_each_lane=1,pixel_to_real_length=0,pixel_height_compensate=0,
                  detected_light_color='',speed_limit=0,left_detection_first_end=0):
    global LINE_CROSSING_DETECTION_POS_TOP
    global LINE_CROSSING_DETECTION_POS_BOTTOM
    
    global IS_LANE_FIRST_AVAILABLE
    global IS_LANE_SECOND_AVAILABLE
    global IS_LANE_THIRD_AVAILABLE
    
    global SPEED_DETECTION_POSITION_LANE_TOP
    global SPEED_DETECTION_POSITION_LANE_BOTTOM
    
    global LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE
    
    global LEFT_DETECTION_POSITION_LANE_FIRST
    global RIGHT_DETECTION_POSITION_LANE_FIRST
    global LEFT_SPEED_DETECTION_POSITION_LANE_FIRST
    global RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST
    
    global LEFT_DETECTION_POSITION_LANE_SECOND
    global RIGHT_DETECTION_POSITION_LANE_SECOND
    global LEFT_SPEED_DETECTION_POSITION_LANE_SECOND
    global RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND
    
    global LEFT_DETECTION_POSITION_LANE_THIRD
    global RIGHT_DETECTION_POSITION_LANE_THIRD
    global LEFT_SPEED_DETECTION_POSITION_LANE_THIRD
    global RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD
    
    global LEAVE_SPEED_DETECTION_POSITION_LANE_TOP
    global LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM
    
    global PIXEL_TO_REAL_LENGTH
    global PIXEL_HEIGHT_COMPENSATE
    
    global DETECTED_LIGHT_COLOR
    
    global SPEED_LIMIT
    
    global LEFT_DETECTION_FIRST_END
    LINE_CROSSING_DETECTION_POS_TOP = line_crossing_detection_pos_top
    LINE_CROSSING_DETECTION_POS_BOTTOM = line_crossing_detection_pos_bottom
    IS_LANE_FIRST_AVAILABLE = is_lane_first_available
    IS_LANE_SECOND_AVAILABLE = is_lane_second_available
    IS_LANE_THIRD_AVAILABLE = is_lane_third_available
    SPEED_DETECTION_POSITION_LANE_TOP=speed_detection_pos_lane_top
    SPEED_DETECTION_POSITION_LANE_BOTTOM=speed_detection_pos_lane_bottom
    LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE=line_crossing_detection_interval_in_each_lane
    LEAVE_SPEED_DETECTION_POSITION_LANE_TOP=leave_speed_detection_position_lane_top
    LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM=leave_speed_detection_position_lane_bottom
    PIXEL_TO_REAL_LENGTH=pixel_to_real_length
    PIXEL_HEIGHT_COMPENSATE=pixel_height_compensate
    DETECTED_LIGHT_COLOR=detected_light_color
    SPEED_LIMIT=speed_limit
    # LEFT_DETECTION_FIRST_END is used to detect doubled solid lines crossing
    LEFT_DETECTION_FIRST_END=left_detection_first_end
    if(IS_LANE_FIRST_AVAILABLE):
        LEFT_DETECTION_POSITION_LANE_FIRST=left_detection_pos_first_start
        RIGHT_DETECTION_POSITION_LANE_FIRST=right_detection_pos_first_end
        
        LEFT_SPEED_DETECTION_POSITION_LANE_FIRST=left_speed_detection_pos_lane_first
        RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST=right_speed_detection_pos_lane_first
    else:
        LEFT_DETECTION_POSITION_LANE_FIRST=0
        RIGHT_DETECTION_POSITION_LANE_FIRST=0
        LEFT_SPEED_DETECTION_POSITION_LANE_FIRST=0
        RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST=0
        
    if(IS_LANE_SECOND_AVAILABLE):
        LEFT_DETECTION_POSITION_LANE_SECOND=left_detection_pos_second_start
        RIGHT_DETECTION_POSITION_LANE_SECOND=right_detection_pos_second_end
        LEFT_SPEED_DETECTION_POSITION_LANE_SECOND=left_speed_detection_pos_lane_second
        RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND=right_speed_detection_pos_lane_second
    else:
        LEFT_DETECTION_POSITION_LANE_SECOND=0
        RIGHT_DETECTION_POSITION_LANE_SECOND=0
        LEFT_SPEED_DETECTION_POSITION_LANE_SECOND=0
        RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND=0
        
    if(IS_LANE_THIRD_AVAILABLE):
        LEFT_DETECTION_POSITION_LANE_THIRD=left_detection_pos_third_start
        RIGHT_DETECTION_POSITION_LANE_THIRD=right_detection_pos_third_end
        
        LEFT_SPEED_DETECTION_POSITION_LANE_THIRD=left_speed_detection_pos_lane_third
        RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD=right_speed_detection_pos_lane_third
    else:
        LEFT_DETECTION_POSITION_LANE_THIRD=0
        RIGHT_DETECTION_POSITION_LANE_THIRD=0 
        LEFT_SPEED_DETECTION_POSITION_LANE_THIRD=0
        RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD=0
def set_current_light_color(light_color):
    global current_light_color
    current_light_color=light_color
    
def vehicle_detect(
    top,
    bottom,
    right,
    left,
    current_frame_number,
    crop_img,
    roi_position,
    ):
    
    speed = -1  # means not available, it is just initialization
    speed_direction=-1 #bottom to top
    
    global is_doubled_solid_line_detection_in_interval
    global last_detected_frame_of_doubled_solid_line_detection
    global is_doubled_solid_line_crossing_detected
    
    global is_vehicle_detected_lane_first_in_interval
    global last_detected_frame_in_lane_first
    global is_vehicle_detected_lane_second_in_interval
    global last_detected_frame_in_lane_second
    global is_vehicle_detected_lane_third_in_interval
    global last_detected_frame_in_lane_third
    
    global last_frame_bottom_position_of_detected_vehicle_in_lane_first
    global current_frame_number_lane_first_list
    global is_in_lane_first
    global is_in_leave_lane_first
    
    global last_frame_bottom_position_of_detected_vehicle_in_lane_second
    global current_frame_number_lane_second_list
    global is_in_leave_lane_second
    global is_in_lane_second

    global last_frame_bottom_position_of_detected_vehicle_in_lane_third
    global current_frame_number_lane_third_list
    global is_in_leave_lane_third
    global is_in_lane_third
    global DETECTED_LIGHT_COLOR
     
    global is_running_red_line
    
    global SPEED_LIMIT
    
    global is_overspeed_detection_in_lane_first_in_interval
    global is_overspeed_detection_in_lane_second_in_interval
    global is_overspeed_detection_in_lane_third_in_interval
    
    global last_detected_overspeed_frame_in_speed_detection_area_first
    global last_detected_overspeed_frame_in_speed_detection_area_second
    global last_detected_overspeed_frame_in_speed_detection_area_third
    
    global is_converse_crossing_in_lane_first_in_interval
    global is_converse_crossing_in_lane_second_in_interval
    global is_converse_crossing_in_lane_third_in_interval
    global detected_pixel_length_of_converse_crossing_in_lane_first
    global detected_pixel_length_of_converse_crossing_in_lane_second
    global detected_pixel_length_of_converse_crossing_in_lane_third
    global last_detected_frame_of_converse_crossing_in_lane_first
    global last_detected_frame_of_converse_crossing_in_lane_second
    global last_detected_frame_of_converse_crossing_in_lane_third
    
    
    
    global LEFT_DETECTION_FIRST_END
    global is_converse_running
    if current_light_color!=DETECTED_LIGHT_COLOR and current_light_color!='black':
        is_running_red_line=True
    else:
        is_running_red_line=False
    #detect crossing double solid line  vehicle
    #using (right-left)length to judge whether vehicle is turning  default length is 500
    is_doubled_solid_line_crossing_detected=[0]
    is_converse_running=False
    
    if(bottom>LINE_CROSSING_DETECTION_POS_BOTTOM):
        if(left<(LEFT_DETECTION_POSITION_LANE_FIRST+LEFT_DETECTION_FIRST_END)*0.5 and right>LEFT_DETECTION_POSITION_LANE_FIRST and right-left>WIDTH_OF_TURNING_VEHICLE and right-left<2*WIDTH_OF_TURNING_VEHICLE and is_doubled_solid_line_detection_in_interval==False):
            is_doubled_solid_line_detection_in_interval=True
            print('doubled solid line crossing vehicle detected')
            is_doubled_solid_line_crossing_detected.insert(0, 1)
            last_detected_frame_of_doubled_solid_line_detection=current_frame_number
        if(current_frame_number-last_detected_frame_of_doubled_solid_line_detection>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE and is_doubled_solid_line_detection_in_interval==True):
            is_doubled_solid_line_detection_in_interval=False
    
    #is_doubled_solid_line_detection_in_interval
    #detect line_crosssing vehicles
    if LINE_CROSSING_DETECTION_POS_TOP < bottom \
        and bottom < LINE_CROSSING_DETECTION_POS_BOTTOM :
        if(current_frame_number-last_detected_frame_in_lane_first>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE and is_vehicle_detected_lane_first_in_interval==True):
            is_vehicle_detected_lane_first_in_interval=False
        if(left>LEFT_DETECTION_POSITION_LANE_FIRST and right<RIGHT_DETECTION_POSITION_LANE_FIRST
           and is_vehicle_detected_lane_first_in_interval==False):
            is_vehicle_detected_lane_first_in_interval=True
            last_detected_frame_in_lane_first=current_frame_number
            is_vehicle_detected.insert(0, 1)
            print('lane 1 detected')
        if(current_frame_number-last_detected_frame_in_lane_second>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE 
           and is_vehicle_detected_lane_second_in_interval==True):
            is_vehicle_detected_lane_second_in_interval=False
            
        if(left>LEFT_DETECTION_POSITION_LANE_SECOND and right<RIGHT_DETECTION_POSITION_LANE_SECOND and is_vehicle_detected_lane_second_in_interval==False):
            is_vehicle_detected_lane_second_in_interval=True
            last_detected_frame_in_lane_second=current_frame_number
            is_vehicle_detected.insert(0, 1)
            print('lane 2 detected')
        if(current_frame_number-last_detected_frame_in_lane_third>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE and is_vehicle_detected_lane_third_in_interval==True):
            is_vehicle_detected_lane_third_in_interval=False  
        if(left>LEFT_DETECTION_POSITION_LANE_THIRD and right<RIGHT_DETECTION_POSITION_LANE_THIRD and is_vehicle_detected_lane_third_in_interval==False):
            is_vehicle_detected_lane_third_in_interval=True
            last_detected_frame_in_lane_third=current_frame_number
            is_vehicle_detected.insert(0, 1)
            print('lane 3 detected')
        
    #detect whether the vehicle gets into the speed detection area
    if bottom<SPEED_DETECTION_POSITION_LANE_BOTTOM and bottom>SPEED_DETECTION_POSITION_LANE_TOP :
        if left>LEFT_SPEED_DETECTION_POSITION_LANE_FIRST and right<RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST:
            is_in_lane_first=True
            pixel_first_length = speed_direction*(bottom - last_frame_bottom_position_of_detected_vehicle_in_lane_first[0])
            #by determining whether the pixel_first_length is postive or not to judge whether the vehicle is converse running
            detected_pixel_length_of_converse_crossing_in_lane_first.insert(0,pixel_first_length)
            if(pixel_first_length<0):
                if(len(detected_pixel_length_of_converse_crossing_in_lane_first)>2):
                    #as sometimes the position returned by Tensorflow may have deviation which will lead to negative result,we should judge the result more than 1 times to avoid this error
                    if(detected_pixel_length_of_converse_crossing_in_lane_first[0]<0 and detected_pixel_length_of_converse_crossing_in_lane_first[1]<0 and detected_pixel_length_of_converse_crossing_in_lane_first[2]<0 and abs(detected_pixel_length_of_converse_crossing_in_lane_first[0]-detected_pixel_length_of_converse_crossing_in_lane_first[1])<50):
                        if(is_converse_crossing_in_lane_first_in_interval==False):
                            print(detected_pixel_length_of_converse_crossing_in_lane_first)
                            print('converse running !')
                            last_detected_frame_of_converse_crossing_in_lane_first.insert(0,current_frame_number)
                            is_converse_running=True
                            is_converse_crossing_in_lane_first_in_interval=True
                            detected_pixel_length_of_converse_crossing_in_lane_first=[0]
                    if(current_frame_number-last_detected_frame_of_converse_crossing_in_lane_first[0]>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE and is_converse_crossing_in_lane_first_in_interval==True):
                            is_converse_crossing_in_lane_first_in_interval=False
            if pixel_first_length>0 and current_frame_number_lane_first_list[0]!=0:
                offset_first_lane=speed_direction*(bottom - LINE_CROSSING_DETECTION_POS_BOTTOM)*PIXEL_HEIGHT_COMPENSATE
                total_frame_passed = current_frame_number - current_frame_number_lane_first_list[0]
                if(total_frame_passed > 0):
                    scale_real_length = pixel_first_length * (PIXEL_TO_REAL_LENGTH+offset_first_lane)
                    if(scale_real_length>0 and is_overspeed_detection_in_lane_first_in_interval==False):
                        # 1 frame=1 /FPS(25)second ,so time= (total_frame_passed * 1)/25
                        #speed=length/time=(total_length_passed/total_frame_passed/25)=(total_length_passed*25)/total_frame_passed
                        speed = (scale_real_length*FPS/total_frame_passed)
                        speed = (speed * 3.6)
                        if(speed>=SPEED_LIMIT):
                            print(speed)
                            is_overspeed_detection_in_lane_first_in_interval=True   
                        #print('car1 ',speed)
            last_frame_bottom_position_of_detected_vehicle_in_lane_first.insert(0, bottom)
            current_frame_number_lane_first_list.insert(0,current_frame_number)
        if left>LEFT_SPEED_DETECTION_POSITION_LANE_SECOND and right<RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND:
            is_in_lane_second=True 
            pixel_second_length = speed_direction*(bottom - last_frame_bottom_position_of_detected_vehicle_in_lane_second[0])
            detected_pixel_length_of_converse_crossing_in_lane_second.insert(0,pixel_second_length)
            if(pixel_second_length<0):
                if(len(detected_pixel_length_of_converse_crossing_in_lane_second)>2):
                    #as sometimes the position returned by Tensorflow may have deviation which will lead to negative result,we should judge the result more than 1 times to avoid this error
                    if(detected_pixel_length_of_converse_crossing_in_lane_second[0]<0 and detected_pixel_length_of_converse_crossing_in_lane_second[1]<0 and detected_pixel_length_of_converse_crossing_in_lane_second[2]<0 and abs(detected_pixel_length_of_converse_crossing_in_lane_second[0]-detected_pixel_length_of_converse_crossing_in_lane_second[1])<50):
                        if(is_converse_crossing_in_lane_second_in_interval==False):
                            print(detected_pixel_length_of_converse_crossing_in_lane_second)
                            print('converse running !')
                            last_detected_frame_of_converse_crossing_in_lane_second.insert(0,current_frame_number)
                            is_converse_running=True
                            is_converse_crossing_in_lane_second_in_interval=True
                            detected_pixel_length_of_converse_crossing_in_lane_second=[0]
                    if(current_frame_number-last_detected_frame_of_converse_crossing_in_lane_second[0]>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE and is_converse_crossing_in_lane_second_in_interval==True):
                            is_converse_crossing_in_lane_second_in_interval=False
            if pixel_second_length>0 and current_frame_number_lane_second_list[0]!=0:
                offset_second_lane=speed_direction*(bottom - LINE_CROSSING_DETECTION_POS_BOTTOM)*PIXEL_HEIGHT_COMPENSATE
                total_frame_passed = current_frame_number - current_frame_number_lane_second_list[0]
                if(total_frame_passed > 0):
                    scale_real_length = pixel_second_length * (PIXEL_TO_REAL_LENGTH+ offset_second_lane)
                    if(scale_real_length>0 and is_overspeed_detection_in_lane_second_in_interval==False):
                        speed = (scale_real_length*FPS/total_frame_passed)
                        speed = (speed * 3.6)
                        if(speed>=SPEED_LIMIT):
                            print(speed)
                            is_overspeed_detection_in_lane_second_in_interval=True
            last_frame_bottom_position_of_detected_vehicle_in_lane_second.insert(0, bottom)
            current_frame_number_lane_second_list.insert(0,current_frame_number)

        if left>LEFT_SPEED_DETECTION_POSITION_LANE_THIRD and right<RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD:
            is_in_lane_third=True
            pixel_third_length = speed_direction*(bottom - last_frame_bottom_position_of_detected_vehicle_in_lane_third[0])
            detected_pixel_length_of_converse_crossing_in_lane_third.insert(0,pixel_third_length)
            if(pixel_third_length<0):
                if(len(detected_pixel_length_of_converse_crossing_in_lane_third>2)):
                    #as sometimes the position returned by Tensorflow may have deviation which will lead to negative result,we should judge the result more than 1 times to avoid this error
                    if(detected_pixel_length_of_converse_crossing_in_lane_third[0]<0 and detected_pixel_length_of_converse_crossing_in_lane_third[1]<0 and detected_pixel_length_of_converse_crossing_in_lane_third[2]<0 and abs(detected_pixel_length_of_converse_crossing_in_lane_third[0]-detected_pixel_length_of_converse_crossing_in_lane_third[1])<50):
                        if(is_converse_crossing_in_lane_third_in_interval==False):
                            print(detected_pixel_length_of_converse_crossing_in_lane_third)
                            print('converse running !')
                            last_detected_frame_of_converse_crossing_in_lane_third.insert(0,current_frame_number)
                            is_converse_running=True
                            is_converse_crossing_in_lane_third_in_interval=True
                            detected_pixel_length_of_converse_crossing_in_lane_third=[0]
                    if(current_frame_number-last_detected_frame_of_converse_crossing_in_lane_third[0]>LINE_CROSSING_DETECTION_INTERVAL_IN_EACH_LANE and is_converse_crossing_in_lane_third_in_interval==True):
                            is_converse_crossing_in_lane_third_in_interval=False
            if pixel_third_length>0 and current_frame_number_lane_third_list[0]!=0:
                offset_third_lane=speed_direction*(bottom - LINE_CROSSING_DETECTION_POS_BOTTOM)*PIXEL_HEIGHT_COMPENSATE
                total_frame_passed = current_frame_number - current_frame_number_lane_third_list[0]
                if(total_frame_passed > 0):
                    scale_real_length = pixel_third_length * (PIXEL_TO_REAL_LENGTH+ offset_third_lane)
                    if(scale_real_length>0 and is_overspeed_detection_in_lane_third_in_interval==False):
                        speed = (scale_real_length*FPS/total_frame_passed)
                        speed = (speed * 3.6)
                        if(speed>=SPEED_LIMIT):
                            print(speed)
                            is_overspeed_detection_in_lane_third_in_interval=True                           
                        #print('car3 ',speed,last_frame_bottom_position_of_detected_vehicle_in_lane_third[0],bottom,current_frame_number,current_frame_number_lane_third_list[0])
                
    #detect whether the vehicle gets into the leave detection area
    if bottom<LEAVE_SPEED_DETECTION_POSITION_LANE_BOTTOM and bottom>LEAVE_SPEED_DETECTION_POSITION_LANE_TOP:
        if left>LEFT_SPEED_DETECTION_POSITION_LANE_FIRST and right<RIGHT_SPEED_DETECTION_POSITION_LANE_FIRST and is_in_lane_first==True:
            is_in_leave_lane_first=True
            is_in_lane_first=False
            if(is_in_leave_lane_first==True and is_in_lane_first==False):
                print('vehicle in lane 1 leave')
                is_overspeed_detection_in_lane_first_in_interval=False
                #clear the last vehicle pos info list
                current_frame_number_lane_first_list=[0]
                last_frame_bottom_position_of_detected_vehicle_in_lane_first=[0]
                is_in_leave_lane_first=False
        if left>LEFT_SPEED_DETECTION_POSITION_LANE_SECOND and right<RIGHT_SPEED_DETECTION_POSITION_LANE_SECOND and is_in_lane_second==True:
            is_in_leave_lane_second=True
            is_in_lane_second=False
            if(is_in_leave_lane_second==True and is_in_lane_second==False):
                print('vehicle in lane 2 leave')
                is_overspeed_detection_in_lane_second_in_interval=False
                current_frame_number_lane_second_list=[0]
                last_frame_bottom_position_of_detected_vehicle_in_lane_second=[0]
                is_in_leave_lane_second=False
                
        if left>LEFT_SPEED_DETECTION_POSITION_LANE_THIRD and right<RIGHT_SPEED_DETECTION_POSITION_LANE_THIRD and is_in_lane_third==True:
            is_in_leave_lane_third=True
            is_in_lane_third=False
            if(is_in_leave_lane_third==True and is_in_lane_third==False):
                print('vehicle in lane 3 leave')
                is_overspeed_detection_in_lane_second_in_interval=False
                current_frame_number_lane_third_list=[0]
                last_frame_bottom_position_of_detected_vehicle_in_lane_third=[0]
                is_in_leave_lane_third=False
    
    return (speed, is_vehicle_detected,is_running_red_line,is_doubled_solid_line_crossing_detected,is_converse_running)
