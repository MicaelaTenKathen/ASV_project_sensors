/*  
 *  ------ [ZB_03] - send packets to a gateway -------- 
 *  
 *  Explanation: This program shows how to send packets to a gateway
 *  indicating the MAC address of the receiving XBee module.  
 *  
 *  Copyright (C) 2015 Libelium Comunicaciones Distribuidas S.L. 
 *  http://www.libelium.com 
 *  
 *  This program is free software: you can redistribute it and/or modify 
 *  it under the terms of the GNU General Public License as published by 
 *  the Free Software Foundation, either version 3 of the License, or 
 *  (at your option) any later version. 
 *  
 *  This program is distributed in the hope that it will be useful, 
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of 
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 *  GNU General Public License for more details. 
 *  
 *  You should have received a copy of the GNU General Public License 
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>. 
 *  
 *  Version:           0.2
 *  Design:            David Gascón 
 *  Implementation:    Yuri Carmona
 */

#include <WaspXBeeZB.h>
#include <WaspFrame.h>
#include <smartWaterIons.h>

// Destination MAC address
//////////////////////////////////////////
char RX_ADDRESS[] = "0013A20041984654";
//////////////////////////////////////////

// Define the Waspmote ID
char WASPMOTE_ID[] = "SW3";


// define variable
uint8_t error;

float temp;

pt1000Class TemperatureSensor;

float no3;
float nh4;

socket1Class NH4Sensor;

// Calibration concentrations solutions used in the process
#define point1_NH4 4.0
#define point2_NH4 20.0
#define point3_NH4 40.0

// Calibration Voltage values
#define point1_volt_NH4 2.424
#define point2_volt_NH4 2.407
#define point3_volt_NH4 2.449

// Define the number of calibration points
#define numPoints 3

float calConcentrations_NH4[] = {point1_NH4, point2_NH4, point3_NH4};
float calVoltages_NH4[] = {point1_volt_NH4, point2_volt_NH4, point3_volt_NH4}; 

socket2Class NO3Sensor;

#define point1_NO3 10.0
#define point2_NO3 100.0
#define point3_NO3 1000.0

// Calibration Voltage values
#define point1_volt_NO3 3.34
#define point2_volt_NO3 3.372
#define point3_volt_NO3 3.492

// Define the number of calibration points
#define numPoints 3

float calConcentrations_NO3[] = {point1_NO3, point2_NO3, point3_NO3};
float calVoltages_NO3[] = {point1_volt_NO3, point2_volt_NO3, point3_volt_NO3}; 

void checkNetworkParams()
{
  xbeeZB.getOperating64PAN();
  xbeeZB.getAssociationIndication();

  while( xbeeZB.associationIndication != 0 )
  {
    delay(2000);

    xbeeZB.getOperating64PAN();

    USB.print(F("operating 64-b PAN ID:"));
    USB.printHex(xbeeZB.operating64PAN[0]);
    USB.printHex(xbeeZB.operating64PAN[1]);
    USB.printHex(xbeeZB.operating64PAN[2]);
    USB.printHex(xbeeZB.operating64PAN[3]);
    USB.printHex(xbeeZB.operating64PAN[4]);
    USB.printHex(xbeeZB.operating64PAN[5]);
    USB.printHex(xbeeZB.operating64PAN[6]);
    USB.printHex(xbeeZB.operating64PAN[7]);
    USB.println();

    xbeeZB.getAssociationIndication();
  }
  USB.println(F("\nJoined a network"));
  
  xbeeZB.getOperating16PAN();
  xbeeZB.getOperating64PAN();
  xbeeZB.getChannel();

  USB.print(F("operating 16-b PAN ID:"));
  USB.printHex(xbeeZB.operating16PAN[0]);
  USB.printHex(xbeeZB.operating16PAN[1]);
  USB.println();
  
  USB.print(F("operating 64-b PAN ID:"));
  USB.printHex(xbeeZB.operating64PAN[0]);
  USB.printHex(xbeeZB.operating64PAN[1]);
  USB.printHex(xbeeZB.operating64PAN[2]);
  USB.printHex(xbeeZB.operating64PAN[3]);
  USB.printHex(xbeeZB.operating64PAN[4]);
  USB.printHex(xbeeZB.operating64PAN[5]);
  USB.printHex(xbeeZB.operating64PAN[6]);
  USB.printHex(xbeeZB.operating64PAN[7]);
  USB.println();

  USB.print(F("channel: "));
  USB.printHex(xbeeZB.channel);
  USB.println();
}

void setup()
{
  // init USB port
  USB.ON();
  USB.println(F("Sending packets example"));
  
  // store Waspmote identifier in EEPROM memory
  frame.setID( WASPMOTE_ID );
  SWIonsBoard.ON();

  NH4Sensor.setCalibrationPoints(calVoltages_NH4, calConcentrations_NH4, numPoints);
  NO3Sensor.setCalibrationPoints(calVoltages_NO3, calConcentrations_NO3, numPoints);
  
  // init XBee
  xbeeZB.ON();
  
  delay(3000);
  
  //////////////////////////
  // 2. check XBee's network parameters
  //////////////////////////
  checkNetworkParams();
  
}


void loop()
{
  ///////////////////////////////////////////
  // 1. Create ASCII frame
  ///////////////////////////////////////////  

  // create new frame
  frame.createFrame(ASCII);  

  temp = TemperatureSensor.read();

  float NH4Voltage = NH4Sensor.read();
  float NH4concentration = NH4Sensor.calculateConcentration(NH4Voltage);

  float NO3Voltage = NO3Sensor.read();
  float NO3concentration = NO3Sensor.calculateConcentration(NO3Voltage);
  
  // add frame fields

  frame.addSensor(SENSOR_BAT, PWR.getBatteryLevel()); 
  frame.addSensor(SENSOR_WATER_WT, temp);
  frame.addSensor(SENSOR_IONS_NH4, NH4concentration);
  frame.addSensor(SENSOR_IONS_NO3, NO3concentration);

  frame.showFrame();

  USB.println(F("Enviando datos sensores"));
  

  ///////////////////////////////////////////
  // 2. Send packet
  ///////////////////////////////////////////  

  // send XBee packet
  error = xbeeZB.send( RX_ADDRESS, frame.buffer, frame.length );   
  
  // check TX flag
  if( error == 0 )
  {
    USB.println(F("send ok"));
    
    // blink green LED
    Utils.blinkGreenLED();
    
  }
  else 
  {
    USB.println(F("send error"));
    
    // blink red LED
    Utils.blinkRedLED();
  }

  // wait for five seconds
  delay(5000);
}

