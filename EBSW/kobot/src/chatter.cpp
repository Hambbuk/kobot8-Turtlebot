#include "ros/ros.h"
#include "std_msgs/Float32.h"
#include <sstream>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "talker");

  ros::NodeHandle n;

  ros::Publisher chatterX = n.advertise<std_msgs::Float32>("chatterX", 1000);
  ros::Publisher chatterY = n.advertise<std_msgs::Float32>("chatterY", 1000);

  std_msgs::Float32 dx, dy;

  dx.msg = 3.0;
  dy.msg = 1.5;

  chatterX.publish(dx);
  chatterY.publish(dy);
  //while문을 돌지 않고 한번만 보내고 값이 바뀔때까지 대기해야하는 방법?
  /*
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::String msg;

    std::stringstream ss;
    ss << "hello world " << count;
    msg.data = ss.str();

    ROS_INFO("%s", msg.data.c_str());

    chatter_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }
  */

  return 0;
}
