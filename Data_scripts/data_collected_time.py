

def data_collec(total_data, init, sensors, k):
    data = list()
    for i in range(len(total_data)):
        shape = total_data.shape
        if init != shape[0] - 1:
            if (total_data.loc[init + 1, "DATE"] - total_data.loc[init, "DATE"]).total_seconds() < 16:
                data.append(total_data.loc[init, sensors[k]])
                init += 1
            else:
                if total_data.loc[init, "SAMPLE_NUM"] == 255 and (
                        total_data.loc[init + 1, "SAMPLE_NUM"] == 0 or total_data.loc[init + 1, "SAMPLE_NUM"] == 1):
                    num_sample = -1
                else:
                    num_sample = total_data.loc[init, "SAMPLE_NUM"]
                if 0 < total_data.loc[init + 1, "SAMPLE_NUM"] - num_sample <= 2.0:
                    data.append(total_data.loc[init, sensors[k]])
                    init += 1
                else:
                    if 390 < init < 430:
                        data.append(total_data.loc[init, sensors[k]])
                        init += 1
                    if init > 433:
                        data.append(total_data.loc[init, sensors[k]])
                        init += 1
                    else:
                        data.append(total_data.loc[init, sensors[k]])
                        init += 1
                        break
        else:
            break
    return data, init