import numpy as np
import pandas as pd
from datetime import datetime
import scipy.io as sio
import csv
import pickle

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
        if num_timestamp == 0:
            continue
        p_dict = {}
        for j in range(num_timestamp):
            p_dict[person[j,0][0]] = [person[j,1][0][0],person[j,2][0][0]] # person[time]=[location, loc_id]
        all_data[str(i)] = p_dict
        tot_data_points += len(p_dict)
    
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

    print("//TODO: STAGE 2: get rid of people who have less than 75% of average data points")
    
    with open('processed.pickle', 'wb') as handle:
        pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("         - done dumping to pickle")

if __name__ == '__main__':
    preprocess()
