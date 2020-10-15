import numpy as np
import pandas as pd
from datetime import datetime
#import requests
import scipy.io as sio
import csv
#import matlab.engine
#eng = matlab.engine.start_matlab()
import pickle

def load_data():
    contents = sio.loadmat('realitymining.mat')
    dated_contents = sio.loadmat('post_data.mat')
    print("done importing contents from matlab")
    #locations = contents['s']['locs']
    loc_ids = contents['s']['loc_ids']
    dated_loc = dated_contents['all_people']

    numPeople = dated_loc.shape[1]
    all_data = {}
    for i in range(numPeople):
        person_count = 0
        person = {}
        for j in range(dated_loc[:,i][0][:,0].shape[0]):
            if len(dated_loc[:,i][0][:,1]) > 0:
                location = dated_loc[:,i][0][:,1][j][0][0]
                l_id = loc_ids[:,i][0][:,0][j]
                person[dated_loc[:,i][0][:,0][j][0]] = [location, l_id] #person[time]=[location, loc_id]
                person_count += 1
        all_data[str(i)] = person

    print(person_count)
    
    print("done processing data")

    example = all_data['2']
    print(example)
    
    with open('processed.pickle', 'wb') as handle:
        pickle.dump(all_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("done dumping to pickle")

if __name__ == '__main__':
    load_data()
