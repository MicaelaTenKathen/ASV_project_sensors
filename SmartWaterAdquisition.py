import serial
import time
from datetime import datetime
import pandas as pd

sensor_keys = ['SAMPLE_NUM', 'BAT', 'WT', 'PH', 'DO', 'COND', 'ORP', 'DATE', 'SWINO3', 'SWINH4']


class WaterQualityModule():
    """ Class for the water quality module sensor aka Libellium. """

    def __init__(self, USB_string='USBPort1', timeout=10000, baudrate=115200):

        """ Create the serial object """
        self.serial = serial.Serial(USB_string, baudrate, timeout=timeout)

        """ Initialize the data dictionary of the sensor measurements """
        self.sensor_data = {}
        for key in sensor_keys:
            self.sensor_data[key] = -1  # A -1 value indicates a faulty value #

    def take_a_sample(self, num_of_samples):
        """ Take num_of_samples and save the data with the given position in the database """

        """ Creamos diccionario pandas """

        # vector of strings that go into db
        sample_num_vector = []
        bat_vector = []
        wt_vector = []
        ph_vector = []
        do_vector = []
        cond_vector = []
        orp_vector = []
        date_vector = []
        no3_vector = []
        nh4_vector = []

        # Iterate over the sample_nums
        for i in range(num_of_samples):
            print("Taking sample {} / {}".format(i + 1, num_of_samples))

            self.read_frame()  # Read a frame from the buffer

            str_date = str(datetime.now())  # Leemos la fecha y la convertimos en string
            # Metemos la fecha en el diccionario de variables
            self.sensor_data['DATE'] = str_date

            print("Incoming data: ")
            print(self.sensor_data)

            # creamos una tupla de parametros que nos permitira introducir los datos en la tabla sensor
            #  ['SAMPLE_NUM','BAT','WT','PH','DO','COND','ORP','DATE','SWINO3','SWINH4']
            sample_num_vector.append(self.sensor_data['SAMPLE_NUM'])
            bat_vector.append(self.sensor_data['BAT'])
            wt_vector.append(self.sensor_data['WT'])
            ph_vector.append(self.sensor_data['PH'])
            do_vector.append(self.sensor_data['DO'])
            cond_vector.append(self.sensor_data['COND'])
            orp_vector.append(self.sensor_data['ORP'])
            date_vector.append(self.sensor_data['DATE'])
            no3_vector.append(self.sensor_data['SWINO3'])
            nh4_vector.append(self.sensor_data['SWINH4'])

        DF = pd.DataFrame(
            {'SAMPLE_NUM': sample_num_vector,
             'Bateria': bat_vector,
             'Temperatura': wt_vector,
             'Ph': ph_vector,
             'Oxigeno Disuelto': do_vector,
             'Conductividad': cond_vector,
             'OxRed': orp_vector,
             'Fecha': date_vector,
             'Nitrato Disuelto': no3_vector,
             'Amonio disuelto': nh4_vector
             }
        )

        return DF

    def read_frame(self):

        is_frame_ok = False  # While a frame hasnt correctly readed #
        self.serial.reset_input_buffer()  # Erase the input buffer to start listening

        while not is_frame_ok:

            time.sleep(0.5)  # Polling time. Every 0.5 secs, check the buffer #

            if self.serial.inWaiting() < 27:  # If the frame has a lenght inferior to the minimum of the Header
                continue

            else:

                try:
                    bytes = self.serial.read_all()  # Read all the buffer #

                    bytes = bytes.decode('ascii', 'ignore')  # Convert to ASCII and ignore non readible characters

                    frames = bytes.split('<=>')  # Frame separator

                    last_frame = frames[-1].split('#')[
                                 :-1]  # Select the last frame, parse the fields (#) and discard the last value (EOF)

                    for field in last_frame:  # Iterate over the frame fields

                        data = field.split(':')
                        if len(data) < 2:
                            # This is not a data field #
                            pass
                        else:
                            # This is a data field #
                            sensor_str = data[0]
                            sensor_val = float(data[1])
                            if sensor_str in sensor_keys:  # The sensor is in the available sensors #
                                self.sensor_data[sensor_str] = sensor_val  # Update the sensor_data dict

                    is_frame_ok = True

                except Exception as E:

                    print("ERROR READING THE SENSOR. THIS IS NO GOOD!")
                    self.serial.reset_input_buffer()

    def close(self):

        print("Cerrando puerto serie!")
        self.serial.close()  # Cerramos la com. serie
        print("Puerto serie cerrado!")

    def __del__(self):

        print("Cerrando puerto serie!")
        self.serial.close()  # Cerramos la com. serie
        print("Puerto serie cerrado!")


if __name__ == '__main__':
    smart_water = WaterQualityModule(USB_string='COM5', timeout=6, baudrate=115200)

    num_of_samples = 1000

    datos = smart_water.take_a_sample(num_of_samples=num_of_samples)

    datos.to_csv('./Data/datapoint(1612).csv')
