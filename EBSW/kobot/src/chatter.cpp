#include "ros/ros.h"
#include "std_msgs/Float32.h"
#include <sstream>
#include <iostream>


/*
0번 위치 0 ,0
1번 위치 2, 2
2번 위치 -1, 2
3번 위치 0, -2
*/
int sector_number, sector_x, sector_y;  //이동해야할 위치
int current_number = 0, current_x = 0, current_y = 0;  //현재 위치
std_msgs::Float32 dx, dy;

int main(int argc, char **argv)
{
  ros::init(argc, argv, "talker");


  //퍼블리셔 핸들러
  ros::NodeHandle n;

  //X에 대한 퍼블리셔
  ros::Publisher chatterX = n.advertise<std_msgs::Float32>("chatterX", 1000);
  
  //Y에 대한 퍼블리셔
  ros::Publisher chatterY = n.advertise<std_msgs::Float32>("chatterY", 1000);

  //임시로 구역에 대한 번호 전달
  std::cin >> sector_number;

  //이동중일때는 어떻게???
  //한번 좌표를 보냈다면 계속 보내면 안되는데 어떻게 확인을 할까?
  //-> 고민할 필요 없을듯 이동하는 동안은 다른 노드를 실행 안할텐데
  switch(sector_number){
  //기본자리
  case 0:
    sector_x = 0;
    sector_y = 0;
  //1번째 자리
  case 1:
    
  
  //2번째 자리
  case 2:

  //3번째 자
  case 3:

  //현재 자리 유지
  case -1;
    
  }    


  //이동해야하는 값 설정
  dx.msg = 3.0;
  dy.msg = 1.5;

  //이동해야하는 값 전송
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
