import pickle
import numpy as np
from scipy.special import softmax
import random

def transition_matrix():

    #import data from hourly_data
    file_in = open("hourly_data.pickle",'rb')
    hourly_data = pickle.load(file_in)  #hourly_data: dict{'id': [data]}
    file_in.close()

    trans_Ms = {}
    #trans_Ms = {'p_id': np.arary(6, num_tags, num_tags), ...}
    i = 0

    max_dim = find_dim(hourly_data)

    num_tags = int(max_dim/100) + 2
    tags = create_tags(hourly_data, num_tags)
    
    #creating transition_matrix for every people
    for p_id, person in hourly_data.items():
        #person: dict {datetime: [time, loc, loc_id, duration]}
        i += 1
        trans_Ms[p_id] = get_person_matrix(i, p_id, person, tags, num_tags + 1)

    with open('diff_time_matrix.pickle', 'wb') as handle:
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

def create_tags(hourly_data, num_tags):
    all_id = {}
    for person in hourly_data.values():
        [p_home, p_work] = find_home_work(person)
        for data in person.values():
            if len(data) > 3 and data[2] not in all_id:
                random.seed(7)
                all_id[data[2]] = str(random.randint(2,num_tags))
            if p_work != 'null':
                all_id[p_work] = '1'
            if p_home != 'null':
                all_id[p_home] = '0'
    print("num loc_id = {}".format(len(all_id)))
    return all_id

def find_home_work(person):
    home = 'null'
    work = 'null'
    freq_count = {}
    for data in person.values():
        if len(data) > 3 and data[2] not in freq_count:
            freq_count[data[2]] = 1
        if len(data) > 3 and data[2] in freq_count:
            freq_count[data[2]] += 1
    sorted_freq = sorted(freq_count, key=freq_count.get, reverse=True)[:2]
    if len(sorted_freq) > 1:
        home = sorted_freq[0]
    if len(sorted_freq) > 2:
        home = sorted_freq[1]
    return [home,work]

def count_loc(trans_Ms):
    all_loc_count = {}
    for p_id in trans_Ms:
        person = trans_Ms[p_id]
        loc_count = {}
        for time_situation in range(6):
            num_locId = person[time_situation].shape[0]
            for loc_id in range(num_locId):
                loc_list = person[time_situation][loc_id]
                if loc_id not in loc_count:
                    loc_count[loc_id] = 0 #initialize with integer value
                loc_count[loc_id] += np.sum(loc_list)

        all_loc_count[p_id] = loc_count


def get_person_matrix(i, p_id, person, tags, num_dim):
    # initialize variables
    matrices = np.empty((6, num_dim, num_dim))
    weekday_night = np.zeros((num_dim,num_dim)) # 12AM - 8AM
    weekend_night = np.zeros((num_dim,num_dim))
    weekday_morn = np.zeros((num_dim,num_dim)) # 8AM - 4PM
    weekend_morn = np.zeros((num_dim,num_dim))
    weekday_aftn = np.zeros((num_dim,num_dim)) # 4PM - 12AM
    weekend_aftn = np.zeros((num_dim,num_dim))

    prev = {'date': list(person.keys())[0].date(), 'loc': -1}
    curr = {'date': list(person.keys())[0].date(), 'loc': -1}

    for time in person:
        curr['date'] = time.date()
        hour = time.hour
        try:
            curr['loc'] = person[time][2]
        except IndexError:
            curr['loc'] = -1

        if prev['loc'] == -1:
            prev['loc'] = curr['loc']
            continue

        prev_fac = int(tags[prev['loc']])
        curr_fac = int(tags[curr['loc']])

        if curr['date'].weekday() < 5:
            if hour < 8 and hour > 0:
                weekday_night[prev_fac, curr_fac] += 1
                #matrices[0,prev_fac, curr_fac] += 1
            elif hour > 8 and hour < 16:
                weekday_morn[prev_fac, curr_fac] += 1
                #matrices[1,prev_fac, curr_fac] += 1
            else:
                weekday_aftn[prev_fac, curr_fac] += 1
                #matrices[2,prev_fac, curr_fac] += 1
        else:
            if hour < 8 and hour > 0:
                weekend_night[prev_fac, curr_fac] += 1
                #matrices[3,prev_fac, curr_fac] += 1
            elif hour > 8 and hour < 16:
                weekend_morn[prev_fac, curr_fac] += 1
                #matrices[4,prev_fac, curr_fac] += 1
            else:
                weekend_aftn[prev_fac, curr_fac] += 1
                #matrices[5,prev_fac, curr_fac] += 1
            
        prev['loc'] = curr['loc']  #move the current location
        prev['date'] = curr['date']  #go to the next day if the date is different

        # scale to probability matrix (row sum to 1)
        # according to definition of transition matrix
        # sum of all probability from one place to other should be 1
        
    #matrices_s = softmax(matrices, axis=2)
    matrices[0] = softmax(weekday_night, axis = 1)
    matrices[1] = softmax(weekend_night, axis = 1)
    matrices[2] = softmax(weekday_morn, axis = 1)
    matrices[3] = softmax(weekend_morn, axis = 1)
    matrices[4] = softmax(weekday_aftn, axis = 1)
    matrices[5] = softmax(weekend_aftn, axis = 1)

    #trans_M = [weekday_night_s, weekend_night_s, weekday_morn_s, weekend_morn_s, weekday_aftn_s, weekend_aftn_s]
    print("{}. Person {}'s matrices Created".format(i, p_id))
    return matrices
    
if __name__ == '__main__':
    transition_matrix()
