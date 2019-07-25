#include <SoftwareSerial.h>
#include<Wire.h>
#include"cactus_io_BME280_I2C.h"

#define START_1 0x42
#define START_2 0x4d
#define DATA_LENGTH_H        0
#define DATA_LENGTH_L        1
#define PM1_0_ATMOSPHERE_H   8
#define PM1_0_ATMOSPHERE_L   9
#define PM2_5_ATMOSPHERE_H   10
#define PM2_5_ATMOSPHERE_L   11
#define PM10_ATMOSPHERE_H    12
#define PM10_ATMOSPHERE_L    13
#define PM2_5_PARTICLE_H   16
#define PM2_5_PARTICLE_L   17
#define VERSION              26
#define ERROR_CODE           27
#define CHECKSUM             29
byte bytCount1 = 0;
byte bytCount2 = 0;
unsigned char chrRecv;
unsigned char chrData[30];
int PM01;
int PM25;
int PM10;
int led1 = 13; // 노란색
int led2 = 12; // 초록색
int led3 = 8; // 빨간색
BME280_I2C bme;

//SoftwareSerial mySerial(7,6); // Arudino Uno port RX, TX
SoftwareSerial mySerial(2,3); // RX, TX

unsigned int GetPM_Data(unsigned char chrSrc[], byte bytHigh, byte bytLow)
{
   return (chrSrc[bytHigh] << 8) + chrSrc[bytLow];
}

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);//기본 통신 속도가 9600인 제품은 9600으로 수정해 주세요
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.println("PMS7003 Ready ");
  Serial.println("Bosch BME280 Pressure - Humidity - Temp Sensor | cactus.io"); 

  if (!bme.begin()) // 온습도 에러 
  { 
  Serial.println("Could not find a valid BME280 sensor, check wiring!"); 
  while (1); 
  } 

  bme.setTempCal(-1);// 아두이노 작동시 열이 발생해 1도를 낮춤

  Serial.println("Pressure\tHumdity\t\tTemp\ttTemp");
}

void loop() {
    if (mySerial.available())   {
       for(int i = 0; i < 32; i++)     {
           chrRecv = mySerial.read();
           if (chrRecv == START_2 ) { 
              bytCount1 = 2;
              break;
            }
       } 
      if (bytCount1 == 2)
      {
         bytCount1 = 0;
         for(int i = 0; i < 30; i++)
         {
            chrData[i] = mySerial.read();
         } 

         if ( (unsigned int) chrData[ERROR_CODE] == 0 ) 
         {
            PM01  = GetPM_Data(chrData, PM1_0_ATMOSPHERE_H, PM1_0_ATMOSPHERE_L);
            PM25  = GetPM_Data(chrData, PM2_5_ATMOSPHERE_H, PM2_5_ATMOSPHERE_L);
            PM10  = GetPM_Data(chrData, PM10_ATMOSPHERE_H, PM10_ATMOSPHERE_L);
            Serial.print("PM1.0=");
            Serial.print(PM01);
            Serial.print(",PM2.5=");
            Serial.print(PM25);
            Serial.print(",PM10=");
            Serial.println(PM10);
            
            if(PM10 <= 30)
            {
              digitalWrite(led1,LOW);
              digitalWrite(led3,LOW);
              digitalWrite(led2, HIGH);
            }
            if(PM10 <= 80 && PM10 >= 31)
            {
              digitalWrite(led2,LOW);
              digitalWrite(led3,LOW);
              digitalWrite(led1, HIGH);
            }
            if(PM10 <= 150 && PM10 >= 81)
            {
              digitalWrite(led1,LOW);
              digitalWrite(led2,LOW);
              digitalWrite(led3, HIGH);
            }
         }
         else
         {
            Serial.println("PMS7003  ERROR");
         }
      } 
   }
   else
   {
      Serial.println("PMS7003 NOT available");
   }
  
  bme.readSensor(); 
  int val;
  val=analogRead(0);//Read Gas value from analog 0
  
  Serial.print("Gas = "); Serial.println(val,DEC);//Print the value to serial port
  Serial.print(bme.getPressure_MB()); Serial.print(" mb\t"); // Pressure in millibars 
  Serial.print(bme.getHumidity()); Serial.print(" %\t\t"); 
  Serial.print(bme.getTemperature_C()); Serial.print(" *C\t"); 
  Serial.print(bme.getTemperature_F()); Serial.println(" *F"); 

  // Add a 2 second delay. 
  delay(1000); //just here to slow down the output. 
}
