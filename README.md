# delivery_drone
Drone Delivery Application with hector_quadrator and ROS Melodic

ROS Melodic, Gazebo 9 and hector_quadrator are required.

To run :
- create a catkin directory if you already didn't.

- Launch world file with ROS(Of course you can create a new package and copy inner files to there. But you should check all the files for pre written references to old package name).
roslaunch robot_proje city.launch

- Enable motors. 
rosservice call /enable_motors "enable: true" 

- Start the delivery node. (Be careful for package name if you changed it)
rosrun robot_proje hector_control.py 

* locations.txt file will be created in ./.ros/locations.txt if you've opened application with roslaunch.
