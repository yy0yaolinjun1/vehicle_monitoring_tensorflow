import cv2
import os
import sqlite3

current_path = os.getcwd()
video_file_name=''
vehicle_overspeed_count = [0]
vehicle_line_crossing_count=[0]

vehicle_database_count=[0]

db_video_name = current_path+'/vehicle_database.db'
def reset_stored_value():
    global vehicle_overspeed_count
    global vehicle_line_crossing_count
    global vehicle_database_count
    vehicle_overspeed_count=[0]
    vehicle_line_crossing_count=[0]
    vehicle_database_count=[0]
def store_overspeed_car_image(image,predicted_speed,file_name):
    images_stored_path=current_path+'/detected_vehicles_images'
    is_video_directory_exists=os.path.exists(images_stored_path+'/'+file_name)
    if is_video_directory_exists==False:
        video_file_path=images_stored_path+'/'+file_name
        os.makedirs(video_file_path)  
    is_overspeed_directory_exists=os.path.exists(images_stored_path+'/'+file_name+'/overspeed_vehicles')
    if  is_overspeed_directory_exists==False:
        os.makedirs(images_stored_path+'/'+file_name+'/overspeed_vehicles')
    cv2.imwrite(images_stored_path+'/'+file_name+'/overspeed_vehicles/'+'vehicle'
                + str(len(vehicle_overspeed_count)) +'_'+str(int(predicted_speed))+'kmh'+ '.png', image)
    vehicle_overspeed_count.insert(0,1)
    
def store_line_crossing_car_image(image,file_name):
    images_stored_path=current_path+'/detected_vehicles_images'
    is_video_directory_exists=os.path.exists(images_stored_path+'/'+file_name)
    if is_video_directory_exists==False:
        video_file_path=images_stored_path+'/'+file_name
        os.makedirs(video_file_path)
    is_line_crossing_directory_exists=os.path.exists(images_stored_path+'/'+file_name+'/line_crossing_vehicles')
    if is_line_crossing_directory_exists==False:
        os.makedirs(images_stored_path+'/'+file_name+'/line_crossing_vehicles')
    cv2.imwrite(images_stored_path+'/'+file_name+'/line_crossing_vehicles/'+'vehicle'+ str(len(vehicle_line_crossing_count)) + '.png', image)
    vehicle_line_crossing_count.insert(0,1)
def run_query(query, parameters =()):
        with sqlite3.connect (db_video_name) as conn:
            cursor = conn.cursor()
            query_result=cursor.execute(query, parameters)
            conn.commit()
            print('store img to database')
        return query_result
def store_detected_vehicles_into_database(image,file_name,is_line_crossing=0,is_overspeed=0):
    images_stored_path=current_path+'/database_detected_vehicles_images/'
    cv2.imwrite(images_stored_path+file_name+'_'+str(len(vehicle_database_count)) + '.png', image)
    vehicle_name=file_name+'_'+str(len(vehicle_database_count))
    vehicle_database_count.insert(0,1)
    query='INSERT INTO vehicles_info VALUES (NULL,?,?,?,?)'
    parameters=(vehicle_name,is_line_crossing,is_overspeed,file_name)
    run_query(query,parameters)
    
