#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <kobot/Msg.h>

#include <stdio.h>
#include <unistd.h>
#include <termios.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

float dx, dy;
int sector_number;
float sector_x, sector_y;
float s1_x, s1_y, s2_x, s2_y, s3_x, s3_y;
float current_x = 0, current_y = 0;
char current_number = 0;

//어디로 이동할지 체크
void check_sector()
{
  if(current_number == sector_number){
      ROS_INFO("not move");
    }
    //기본자리
    else if(sector_number == 0){
      sector_x = 0;
      sector_y = 0;
      dx= current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 0;
      ROS_INFO("move sector 0");
    }

    //1번째 자리
    else if(sector_number == 1){
      sector_x = s1_x;
      sector_y = s1_y;
      dx = current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 1;
      ROS_INFO("dx : [%f], dy : [%f]", dx, dy);
      ROS_INFO("move sector 1");
    }
          
    //2번째 자리
    else if(sector_number == 2){
      sector_x = s2_x;
      sector_y = s2_y;
      dx = current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 2;
      ROS_INFO("move sector 2");
    }
        
    else if(sector_number == 3){
      sector_x = s3_x;
      sector_y = s3_y;
      dx = current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 3;
      ROS_INFO("move sector 3");
    }
}

void callbackpose(const kobot::Msg::ConstPtr& msg)
{
  s1_x = msg->x1;
  s1_y = msg->y1;
  s2_x = msg->x2;
  s2_y = msg->y2;
  s3_x = msg->x3;
  s3_y = msg->y3;
  sector_number = msg->sector_number;
  ROS_INFO("sector_number : [%f]", msg->sector_number);
}


int main(int argc, char** argv){
  ros::init(argc, argv, "simple_navigation_goals");
  MoveBaseClient ac("move_base", true);
  ros::NodeHandle n;
  ROS_INFO("1");


  while(ros::ok()){
    //1초당 1번씩
    ros::Rate rate(1);
    ros::Subscriber sub_pose;
    int cnt = 0;
    while(ros::ok()){
      cnt ++;
      if(cnt == 1){
        sub_pose = n.subscribe("pose", 1000, callbackpose);
        ROS_INFO("in if publisher");
        cnt = 1;
      }
      if(sector_number != current_number){
        ROS_INFO("in flag==1 and break");
        break;
      }
      ros::spinOnce();
      rate.sleep();
    }
    
    ROS_INFO("2");
    //좌표값받아오는 함수

    //위동할 위치 받아오는 함수
    //sector_number
    //어느 자리로 이동할지 체크

    ROS_INFO("3");

    check_sector();

    //이제부터 움직이는 함수
    while(!ac.waitForServer(ros::Duration(5.0))){
      ROS_INFO("Waiting for the move_base action server to come up");
    }
    move_base_msgs::MoveBaseGoal goal;
    //we'll send a goal to the robot to move 1 meter forward
    goal.target_pose.header.frame_id = "base_link";
    goal.target_pose.header.stamp = ros::Time::now();
    //픽셀 한칸당 5cm 그럼 1m는 가제보나 rviz기준으로 20칸인가?
    goal.target_pose.pose.position.x = dx;
    goal.target_pose.pose.position.y = dy;
    goal.target_pose.pose.orientation.w = 1.0;
    ROS_INFO("Sending goal");
    ac.sendGoal(goal);

    ac.waitForResult();
    
    if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
      ROS_INFO("Hooray, the base moved sector_number %d forward", sector_number);
    else
      ROS_INFO("The base failed to move forward 1 meter for some reason");
  }
  ros::spin();
  //////////////////////////////////////////////////////////////////
  return 0;
}
