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
#include <WaspSensorSW.h>

// Destination MAC address
//////////////////////////////////////////
char RX_ADDRESS[] = "0013A20041DC3580";
//////////////////////////////////////////

// Define the Waspmote ID
char WASPMOTE_ID[] = "SW2";
char node_ID[] = "Temperature_example";


// define variable
uint8_t error;

//Temperature Sensor
float temp;
pt1000Class TemperatureSensor;

//pH Sensor
float pHVol;
float pHValue;

#define cal_point_10  1.980
#define cal_point_7   2.090
#define cal_point_4   2.251

#define cal_temp 20.1

pHClass pHSensor;

//DO Sensor

float DOVol;
float DOValue;

// Calibration of the sensor in normal air
#define air_calibration 3.55
// Calibration of the sensor under 0% solution
#define zero_calibration 0.203

DOClass DOSensor;

//Conductivity Sensor

float ECRes;
float ECValue;

// Value 1 used to calibrate the sensor
#define point1_cond 84
// Value 2 used to calibrate the sensor
#define point2_cond 1413

// Point 1 of the calibration 
#define point1_cal 12964
// Point 2 of the calibration 
#define point2_cal 871

conductivityClass ConductivitySensor;

//ORP Sensor

float ORPValue;

// Offset obtained from sensor calibration
#define calibration_offset 0.019

ORPClass ORPSensor;


/*******************************************
 *
 *  checkNetworkParams - Check operating
 *  network parameters in the XBee module
 *
 *******************************************/
void checkNetworkParams()
{
  // 1. get operating 64-b PAN ID
  xbeeZB.getOperating64PAN();

  // 2. wait for association indication
  xbeeZB.getAssociationIndication();
 
  while( xbeeZB.associationIndication != 0 )
  { 
    delay(500);
    
    // get operating 64-b PAN ID
    xbeeZB.getOperating64PAN();

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


  // 3. get network parameters 
  xbeeZB.getOperating16PAN();
  xbeeZB.getOperating64PAN();
  xbeeZB.getChannel();

  USB.printHex(xbeeZB.operating16PAN[0]);
  USB.printHex(xbeeZB.operating16PAN[1]);

  USB.printHex(xbeeZB.operating64PAN[0]);
  USB.printHex(xbeeZB.operating64PAN[1]);
  USB.printHex(xbeeZB.operating64PAN[2]);
  USB.printHex(xbeeZB.operating64PAN[3]);
  USB.printHex(xbeeZB.operating64PAN[4]);
  USB.printHex(xbeeZB.operating64PAN[5]);
  USB.printHex(xbeeZB.operating64PAN[6]);
  USB.printHex(xbeeZB.operating64PAN[7]);
  USB.println();

}

void setup()
{
  // init USB port
  USB.ON();
  USB.println(F("Sending packets example"));
  
  // store Waspmote identifier in EEPROM memory
  frame.setID( WASPMOTE_ID );

  Water.ON();

  pHSensor.setCalibrationPoints(cal_point_10, cal_point_7, cal_point_4, cal_temp);
  DOSensor.setCalibrationPoints(air_calibration, zero_calibration);
  ConductivitySensor.setCalibrationPoints(point1_cond, point1_cal, point2_cond, point2_cal);
  
  // init XBee
  xbeeZB.ON();
  
  delay(500);
  
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

  temp = TemperatureSensor.readTemperature();

 // Read the ph sensor (voltage value)
  pHVol = pHSensor.readpH();
  // Convert the value read with the information obtained in calibration
  pHValue = pHSensor.pHConversion(pHVol, temp);

    // Reading of the ORP sensor
  DOVol = DOSensor.readDO();
  // Conversion from volts into dissolved oxygen percentage
  DOValue = DOSensor.DOConversion(DOVol);

  ECRes = ConductivitySensor.readConductivity();
  // Conversion from resistance into us/cm
  ECValue = ConductivitySensor.conductivityConversion(ECRes);

  // Reading of the ORP sensor
  ORPValue = ORPSensor.readORP();
  // Apply the calibration offset
  ORPValue = ORPValue - calibration_offset;

  frame.addSensor(SENSOR_BAT, PWR.getBatteryLevel());
  frame.addSensor(SENSOR_WATER_WT, temp);
  frame.addSensor(SENSOR_WATER_PH, pHValue);
  frame.addSensor(SENSOR_WATER_DO, DOValue);
  frame.addSensor(SENSOR_WATER_COND, ECValue);
  frame.addSensor(SENSOR_WATER_ORP, ORPValue);

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
  delay(500);
}






