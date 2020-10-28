import pickle
import numpy as np
import scipy.io as sio
from scipy.special import softmax

def transition_matrix():

    #import data from hourly_data
    file_in = open("hourly_data.pickle",'rb')
    hourly_data = pickle.load(file_in)  #hourly_data: dict{'id': [data]}
    file_in.close()

    trans_Ms = {}
    i = 0

    max_dim = find_dim(hourly_data)

    #creating transition_matrix for every people
    for p_id, person in hourly_data.items():
        #person: dict {datetime: [time, loc, loc_id, duration]}

        # initialize variables
        weekday_M = np.zeros((max_dim,max_dim))
        weekend_M = np.zeros((max_dim,max_dim))
        prev = {'date': list(person.keys())[0].date(), 'loc': -1}
        curr = {'date': list(person.keys())[0].date(), 'loc': -1}

        for time in person:
            curr['date'] = time.date()
            try:
                curr['loc'] = person[time][2]
            except:
                curr['loc'] = -1

            if curr['date'].weekday() < 5:
                if prev['loc'] == -1:
                    prev['loc'] = curr['loc']
                    continue
                weekday_M[prev['loc'], curr['loc']] += 1 
            else:
                if prev['loc'] == -1:
                    prev['loc'] = curr['loc']
                    continue
                weekend_M[prev['loc'], curr['loc']] += 1 
            
            prev['loc'] = curr['loc']  #move the current location
            prev['date'] = curr['date']  #go to the next day if the date is different

        # scale to probability matrix (row sum to 1)
        # according to definition of transition matrix
        # sum of all probability from one place to other should be 1
        weekday_M = softmax(weekday_M, axis = 1)
        weekend_M = softmax(weekend_M, axis = 1)

        trans_Ms[p_id] = [weekday_M, weekend_M]
        i+=1
        print("{}. Person {}'s matrix Created".format(i, p_id))
    
    with open('individual_matrix.pickle', 'wb') as handle:
        pickle.dump(trans_Ms, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("- done dumping to pickle")

def find_dim(hourly_data):
    cur_max = 0
    for person in hourly_data.values():
        for data in person.values():
            if len(data) > 3 and data[2] > cur_max:
                cur_max = data[2]
    print("max loc_id = {}".format(cur_max))
    return cur_max + 1

if __name__ == '__main__':
    transition_matrix()
