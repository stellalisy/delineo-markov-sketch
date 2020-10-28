import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import scipy.io as sio
import csv
import pickle
from operator import itemgetter

def preprocess():
    print("STAGE 1: import data from matlab and reformat")
    contents = sio.loadmat('date_in_str.mat')
    all_people = contents['all_people'] # <class 'numpy.ndarray'> (1,106)
    numPeople = all_people.shape[1]
    print("         - done importing contents from matlab")

    all_data = {}
    tot_data_points = 0
    for i in range(numPeople):
        person = all_people[0,i] # <class 'numpy.ndarray'> (num_timestamp,3)
        num_timestamp = person.shape[0]
        if num_timestamp == 0 or person.shape[1] == 0:
            continue
        p_info = []
        for j in range(num_timestamp):
            try:
                time = person[j,0][0]
            except:
                print("IndexError: index 0 is out of bounds for axis 1 with size 0")
                print(person.shape)
                print("j = {}".format(j))
            #time = time.split('-')
            #time[1] = str(month_cal[time[1]])
            #time = '-'.join(time)
            p_info.append([time, person[j,1][0][0], person[j,2][0][0]]) # p_info = [[time, location, loc_id], ...]
        all_data[str(i)] = p_info
        tot_data_points += len(p_info)
    
    print("         - done reformatting data, total of {} people in the data".format(len(all_data)))
    #example = all_data['2']
    #print(example)

    print("STAGE 2: get rid of people who have less than 75% of average data points")
    avg_dp = tot_data_points/len(all_data)
    threshold = avg_dp * 0.75
    new_dict = {}
    for p_id, p_info in all_data.items():
        if len(p_info) >= threshold:
            new_dict[p_id] = p_info
    print("         - done getting rid of sparse data points, total of {} people in the data".format(len(new_dict)))

    print("STAGE 3: only keep the datapoint of the longest duration in each hour (preliminary)")

    #append duration of each data point to the list
    datetimeFormat = '%d-%b-%Y %H:%M:%S'
    dict_hourly = {}
    num_hourly_dp = 0
    for p_id, p_info in new_dict.items():
        p_hourstamps = {}
        for i in range(len(p_info) - 1):
            try:
                start = datetime.strptime(p_info[i][0], datetimeFormat)
            except:
                continue
            try:
                end = datetime.strptime(p_info[i+1][0], datetimeFormat)
            except:
                try:
                    end = datetime.strptime(p_info[i+2][0], datetimeFormat)
                except:
                    continue
            duration = end - start
            p_info[i].append(duration)
            key = start.replace(minute=0, second=0)
            if key not in p_hourstamps:
                p_hourstamps[key] = [p_info[i]]
            else:
                p_hourstamps[key].append(p_info[i])
        for key_time, item in p_hourstamps.items():
            p_hourstamps[key_time] = sorted(item, key = itemgetter(3))[-1]
        num_hourly_dp += len(p_hourstamps)
        dict_hourly[p_id] = p_hourstamps
    
    avg_hourly = num_hourly_dp / len(dict_hourly)
    print(dict_hourly[list(dict_hourly.keys())[0]])
    print("         - done filtering hourly data, average of {} timestamps per person".format(avg_hourly))

    #with open('processed.pickle', 'wb') as handle:
    #    pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #print("         - done dumping to pickle")
    with open('hourly_data.pickle', 'wb') as handle:
        pickle.dump(dict_hourly, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("         - done dumping to pickle")

if __name__ == '__main__':
    preprocess()
