/*
    ------ Waspmote Pro Code Example --------

    Explanation: This is the basic Code for Waspmote Pro

    Copyright (C) 2016 Libelium Comunicaciones Distribuidas S.L.
    http://www.libelium.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
 *  Design:            José Miguel Córdoba Méndez

// Put your libraries here (#include ...)

#include <smartWaterIons.h>

// Connect the Nitrates Sensor in the SOCKET2
// All Ion sensors can be connected in the four sockets
socket1Class NH4Sensor;

// Calibration concentrations solutions used in the process
#define point1 4.0
#define point2 20.0
#define point3 40.0

// Calibration Voltage values
#define point1_volt_NH4 2.61
#define point2_volt_NH4 2.82
#define point3_volt_NH4 2.90

// Define the number of calibration points
#define numPoints 3

float calConcentrations[] = {point1, point2, point3};
float calVoltages[] = {point1_volt_NH4, point2_volt_NH4, point3_volt_NH4}; 

void setup()
{
  // Turn ON the Smart Water Ions Board and USB
  SWIonsBoard.ON();
  USB.ON();  

  // Calculate the slope and the intersection of the logarithmic function
  NH4Sensor.setCalibrationPoints(calVoltages, calConcentrations, numPoints);
}

void loop()
{
  // Reading of the NO3 sensor
  float NH4Voltage = NH4Sensor.read();

  // Print of the results
  USB.print(F(" NH4 Voltage: "));
  USB.print(NH4Voltage);
  USB.print(F("volts |"));

  float concentration = NH4Sensor.calculateConcentration(NH4Voltage);

  USB.print(F(" NH4 concentration Estimated: "));
  USB.print(concentration);
  USB.println(F(" ppm / mg * L-1"));

  delay(1000);  
}
