#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
#include "geometry_msgs/Twist.h"
#include <iostream>+


#define FORWARD_SPEED_MPS  0.5
#define TURN_SPEED_MPS  1.57//90 degrees equals 1.57 rad
#define MIN_SCAN_ANGLE_RAD  -90.0/180*M_PI
#define MAX_SCAN_ANGLE_RAD  +90.0/180*M_PI

class WallAboider {
    private:
        ros::Subscriber laser_scan_sub;  
        ros::NodeHandle nh;

        float current_angle = 0;
    	const static float final_angle = 1.57 ; //..............FIX THIS FOR TURN
        int t1, t0;


    public:
        WallAboider();
        void laserCallback(const sensor_msgs::LaserScan::ConstPtr& laser);
     
};

WallAboider::WallAboider(){
    laser_scan_sub = nh.subscribe("/scan", 10, &WallAboider::laserCallback,this);
    

}
void WallAboider::laserCallback(const sensor_msgs::LaserScan::ConstPtr& laser){
    
   

   	int minIndex = ceil((MIN_SCAN_ANGLE_RAD - laser->angle_min) / laser->angle_increment);
	int maxIndex = floor((MAX_SCAN_ANGLE_RAD - laser->angle_min) / laser->angle_increment);
	int midIndex = (minIndex + maxIndex) / 2;

	double closestRange_left = laser->ranges[minIndex];
	double closestRange_right = laser->ranges[midIndex];
   	double longestRange_left = 0;
   	double longestRange_right = 0;
    	int avg_left = 0;
    	int avg_right = 0;
    
	for(int currIndex = minIndex + 1; currIndex <= midIndex; currIndex++){
		if(laser->ranges[currIndex] < closestRange_right){
			closestRange_right = laser->ranges[currIndex];
            
		}
        	if(laser->ranges[currIndex] > longestRange_right){
					longestRange_right = laser->ranges[currIndex];
            
		}
        	//avg_right += laser->ranges[currIndex];
	}

   	 //avg_right /= (midIndex-minIndex);

	for(int currIndex = midIndex + 1; currIndex < maxIndex; currIndex++){
		if(laser->ranges[currIndex] < closestRange_left){
			closestRange_left = laser->ranges[currIndex];
           
		}
        	 if(laser->ranges[currIndex] > longestRange_left){
			longestRange_left = laser->ranges[currIndex];
            
		}
       	}

    	ROS_INFO_STREAM("closest_left =	 " << closestRange_left << "closest_right = 	" << closestRange_right);
		ROS_INFO_STREAM("longest_left =  " << longestRange_left << "longest_right = 	" << longestRange_right);
    

}



int main(int argc, char **argv){
    
    ros::init(argc, argv, "robot_controller");
    
    WallAboider wa;

	ros::Rate loop_rate(30);

	loop_rate.sleep();
    
    ros::spin();

    return 0;
} 

