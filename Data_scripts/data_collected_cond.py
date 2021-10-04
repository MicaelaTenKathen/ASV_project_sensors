
def data_collec_cond(total_data, init, sensors, k, conf):
    data = list()
    for i in range(len(total_data)):
        shape = total_data.shape
        if init != shape[0] - 1:
            if total_data.loc[init, "Conductividad"] > 100:
                print('in')
                data.append(total_data.loc[init, sensors[k]])
                init += 1
                conf = True
            else:
                init += 1
                break
        else:
            break
    return data, init, conf
