#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>

#include <stdio.h>
#include <unistd.h>
#include <termios.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

float dx, dy;
int sector_number;
float sector_x, sector_y;
float current_x = 0, current_y = 0;
char current_number = '0';

int getch()
{
  static struct termios oldt, newt;
  tcgetattr( STDIN_FILENO, &oldt);           // save old settings
  newt = oldt;
  newt.c_lflag &= ~(ICANON);                 // disable buffering      
  tcsetattr( STDIN_FILENO, TCSANOW, &newt);  // apply new settings

  int c = getchar();  // read character (non-blocking)

  tcsetattr( STDIN_FILENO, TCSANOW, &oldt);  // restore old settings
  return c;
}

int main(int argc, char** argv){
  ros::init(argc, argv, "simple_navigation_goals");

  //tell the action client that we want to spin a thread by default
  MoveBaseClient ac("move_base", true);
  while(ros::ok()){
    ROS_INFO("you want move sector_numer key");
    sector_number = getch();
    //이동중일때는 어떻게???
    //한번 좌표를 보냈다면 계속 보내면 안되는데 어떻게 확인을 할까?
    
    //같은 자리면 이동 x
    if(current_number == sector_number){
      ROS_INFO("not move");
    }
    //기본자리
    else if(sector_number == '0'){
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
    else if(sector_number == '1'){
      sector_x = -4;
      sector_y = -1;
      dx = current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 1;
      ROS_INFO("move sector 1");
    }
          
    //2번째 자리
    else if(sector_number == '2'){
      sector_x = 3;
      sector_y = 1;
      dx = current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 2;
      ROS_INFO("move sector 2");
    }
        
    else if(sector_number == '3'){
      sector_x = 0;
      sector_y = -2;
      dx = current_x - sector_x;
      dy = current_y - sector_y;
      current_x = sector_x;
      current_y = sector_y;
      current_number = 3;
      ROS_INFO("move sector 3");
    }

    //서버에서 메시지가 올때까지 대기
    while(!ac.waitForServer(ros::Duration(5.0))){
      ROS_INFO("Waiting for the move_base action server to come up");
    }

    move_base_msgs::MoveBaseGoal goal;

    //we'll send a goal to the robot to move 1 meter forward
    goal.target_pose.header.frame_id = "base_link";
    goal.target_pose.header.stamp = ros::Time::now();
    
    //픽셀 한칸당 5cm 그럼 1m는 가제보나 rviz기준으로 20칸인가?
    //현재 좌표를 기준으로 x방향으로 1.0m
    //현재 좌표를 기준으로 y방향으로 2.0m
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
  return 0;
}
