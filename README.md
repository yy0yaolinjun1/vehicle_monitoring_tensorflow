# Traffic Monitoring System
This project is written in python and the vehicle detection is based on Tensorflow_Object_Detection_API
[**Demo Link**](https://www.bilibili.com/video/av48336782/)
<p align="center">
  <img src="https://github.com/yy0yaolinjun1/ScreenShot/blob/master/TrafficMonitoring/main_ui.png">
</p>

## General Capabilities of This Project

1) Real-time traffic monitoring(using ssd_mobilenet_v2 Model,more detection model see here https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

2) Interest Area:only the vehicles in the area will be detected by Tensorflow

3) Speed detection: When the vehicle passes through the speed detection area(The speed of the vehicle on each lane is calculated separately)

4) speeding vehicle capture:When the vehicle speed is over the speed limit, the vehicle will be captured and the relevant info and image will be stored.

5) Recognition of traffic light color:the current color of the traffic light will be recognized
(This part of the code reference from @ONLINE{cr,author="Ahmet Özlü",title="Color Recognition",year="2018",url="https://github.com/ahmetozlu/color_recognition")

6) Cross-line detection and capture: When the vehicle passes the cross-line detection area and the traffic light color is the same as the color we set, the vehicle will be captured and the relevant info and image will be stored.

7) Vehicle leave detection: It is used to judge whether the vehicle on the lane has left. If so, the data of the corresponding lane stored like speed, current frame number, etc will be reset in order to detect the upcoming vehicles.

8) ROI values setting and dynamically previewing the modified effect

9) Saving and loading ROI values

10) viewing the violation records from the database

11) Avoiding repetitive detection(method1: setting the frame interval for each lane. method2: only when the vehicle pass through the leave detection area could the vehicle be detected again)

v1.1 new capabilities
12)Double line crossing detection:(notice: since detecting the vehicle through the width of detected bounding box and because of the perspective projection,
the width of the vehicle bounding box that first appears in the video is large,which may lead to error detection and therefore,modifying the interest area is needed)
<p align="center">
  <img src="https://github.com/yy0yaolinjun1/ScreenShot/blob/master/TrafficMonitoring/double_line_crossing.JPG">
</p>
the image below is the width of bounding box that first appears in lane first after modifying the interest area(the width becomes narrower than before) .
<p align="center">
  <img src="https://github.com/yy0yaolinjun1/ScreenShot/blob/master/TrafficMonitoring/interest_area_modified.JPG">
</p>
13)Converse moving detection:
<p align="center">
  <img src="https://github.com/yy0yaolinjun1/ScreenShot/blob/master/TrafficMonitoring/converse_crossing.jpg">
</p>

## Installation
install tensorflow_cpu
installation guide:(https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest)

ps:pip install missing_package_name,and please press 'q' to quit the preview before running video detection(one of the bugs that needed to be fixed...)