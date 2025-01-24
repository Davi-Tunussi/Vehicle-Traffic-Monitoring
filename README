Vehicle Traffic Monitoring

Overview

This project implements a traffic monitoring system for highways using the OpenCV library. It detects, tracks, and calculates the speed of vehicles in user-defined regions of interest (ROIs). The system also displays each vehicle's speed in pixels/frame and km/h.

Project Structure

Main.py:

Main script that runs the monitoring system.

Data Folder:

Contains the input video for analysis (video_rodovia.mp4).

Output Example Folder:

Includes an example output video of the system in action (Monitoramento_Rodovia.mp4).

Key Features

ROI Definition:

Users manually select regions of interest (ROIs) in the video using the mouse.

Each ROI includes a counting line to detect vehicles crossing it.

Vehicle Detection and Tracking:

Detects moving vehicles using background subtraction and morphological transformations to reduce noise.

Tracks vehicles based on centroids calculated for each frame.

Speed Calculation:

Calculates the speed of each vehicle in:

Pixels/frame (displacement rate in the video).

Km/h (converting to a real-world unit based on pixel length and video frame rate).

Visualization:

Displays vehicle ID, speed, and regions of interest directly on the video.

How to Run

Ensure the input video (video_rodovia.mp4) is located in the Data folder.

Replace the video path in the cap variable in the Main.py script if the video is stored elsewhere.

Install the project dependencies:

pip install opencv-python-headless numpy

Run the Main.py script.

In the displayed video:

Draw ROIs by clicking and dragging the mouse.

Press 'q' to finish the selection.

After selecting the ROIs, the system will start monitoring, displaying:

Bounding boxes on detected vehicles.

ID, speed (in pixels/frame and km/h), and total vehicles for each ROI.

Press 'q' to quit.

Configurable Parameters

min_area: Minimum area to detect a contour as a vehicle (default: 150).

centroid_dist_threshold: Maximum distance between consecutive centroids to track a vehicle (default: 50 pixels).

pixel_length: Length of each pixel in cm (default: 7.2 cm).

frames_per_second: Video frame rate (default: 30 fps).

Example Output

When running the script, the video will be processed and display information such as:

ROI 1: Total: 5
ROI 2: Total: 3
ID: 1, Vel: 12.50 px/frame, 32.40 km/h
ID: 2, Vel: 10.25 px/frame, 26.40 km/h

Notes

Ensure the provided video has good quality for efficient detection.

The system is designed to run in real time, but performance may vary depending on video resolution and hardware capacity.

Author

This project was developed to monitor and analyze highway traffic, providing accurate data on vehicle count and speed.

