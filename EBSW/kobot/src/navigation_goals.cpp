#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

float dx, dy;

void callbackX(const std_msgs::Float32::ConstPtr& msg)
{
  ROS_INFO("I heard dx: [%f]", msg->data);
  dx = msg->data;
}

void callbackY(const std_msgs::Float32::ConstPtr& msg)
{
  ROS_INFO("I heard dy : [%f]", msg->data);
  dy = msg->data;
}

int main(int argc, char** argv){
  ros::init(argc, argv, "simple_navigation_goals");

  //서브스크리버 핸들러
  ros::NodeHandle n;
  
  //x에 대한 서브스크리버
  ros::Subscriber subx = n.subscribe("chatterX", 1000, callbackX);

  //y에 대한 서브스크리버
  ros::Subscriber suby = n.subscribe("chatterY", 1000, callbackY);

  //tell the action client that we want to spin a thread by default
  MoveBaseClient ac("move_base", true);

  //서버에서 메시지가 올때까지 대기
  while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  //이동량이 없어도 대기???

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
    ROS_INFO("Hooray, the base moved 1 meter forward");
  else
    ROS_INFO("The base failed to move forward 1 meter for some reason");

  //퍼블리셔한테 콜백을 지속적으로 요청
  ros::spin();

  return 0;
}
