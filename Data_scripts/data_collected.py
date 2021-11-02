class Data_collected(object):
    def __init__(self, total_data, sensors):
        self.total_data = total_data
        self.sensors = sensors

    def data_collec(self, k, initial):
        data = list()
        for i in range(len(self.total_data)):
            shape = self.total_data.shape
            if initial != shape[0] - 1:
                if (self.total_data.loc[initial + 1, "DATE"] - self.total_data.loc
                [initial, "DATE"]).total_seconds() < 16:
                    data.append(self.total_data.loc[initial, self.sensors[k]])
                    initial += 1
                else:
                    if self.total_data.loc[initial, "SAMPLE_NUM"] == 255 and (
                            self.total_data.loc[initial + 1, "SAMPLE_NUM"] == 0 or self.total_data.loc
                    [initial + 1, "SAMPLE_NUM"] == 1):
                        num_sample = -1
                    else:
                        num_sample = self.total_data.loc[initial, "SAMPLE_NUM"]
                    if 0 < self.total_data.loc[initial + 1, "SAMPLE_NUM"] - num_sample <= 2.0:
                        data.append(self.total_data.loc[initial, self.sensors[k]])
                        initial += 1
                    else:
                        if 390 < initial < 430:
                            data.append(self.total_data.loc[initial, self.sensors[k]])
                            initial += 1
                        if initial > 433:
                            data.append(self.total_data.loc[initial, self.sensors[k]])
                            initial += 1
                        else:
                            data.append(self.total_data.loc[initial, self.sensors[k]])
                            initial += 1
                            break
            else:
                break
        return data, initial

    def data_collec_cond(self, initial, k, conf):
        data = list()
        for i in range(len(self.total_data)):
            shape = self.total_data.shape
            if initial != shape[0] - 1:
                if self.total_data.loc[initial, "Conductividad"] > 100:
                    print('in')
                    data.append(self.total_data.loc[initial, self.sensors[k]])
                    initial += 1
                    conf = True
                else:
                    initial += 1
                    break
            else:
                break
        return data, conf, initial

    def data_collec_no3(self, initial, k, conf):
        data = list()
        for i in range(len(self.total_data)):
            shape = self.total_data.shape
            if initial != shape[0] - 1:
                if self.total_data.loc[initial, "Nitrato Disuelto"] > 0:
                    print('in')
                    data.append(self.total_data.loc[initial, self.sensors[k]])
                    initial += 1
                    conf = True
                else:
                    initial += 1
                    break
            else:
                break
        return data, conf, initial
