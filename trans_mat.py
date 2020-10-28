import numpy as np
import scipy.io as sio
from scipy.special import softmax
import pickle

def transition_matrix():

    #import data from hourly_data
    hourly_data = []
    with (open("hourly_data.pickle", "rb")) as openfile:
        while True:
            try:
                hourly_data.append(pickle.load(openfile))
            except EOFError:
                break
    # initialize transition matrix list
    trans_Ms = []
    i = 0
    #creating transition_matrix for every people
    for people in hourly_data[0]:

        # initialize variable
        trans_M = np.zeros((3108,3108))
        previous_date = ""
        previous_loc = -1
        curr_date = ""
        curr_loc = -1

        for date in hourly_data[0].get(people):
            curr_date = hourly_data[0].get(people).get(date)[0]
            # exclude different date situation
            if curr_date[:11] == previous_date[:11]:
                curr_loc = hourly_data[0].get(people).get(date)[2]
                trans_M[previous_loc, curr_loc] = trans_M[previous_loc, curr_loc] + 1
                previous_loc = curr_loc
            else:
                previous_loc = curr_loc
                previous_date = curr_date

        # scale to probability matrix (row sum to 1)
        # according to definition of transition matrix
        # sum of all probability from one place to other should be 1
        trans_M = softmax(trans_M, axis = 1)
        trans_Ms.append(trans_M)
        i+=1
        print("Person " + str(i) + " matrix Created")
    print(trans_Ms)
if __name__ == '__main__':
    transition_matrix()
