import numpy as np
import scipy.io as sio
from scipy.special import softmax
def transition_matrix():

    #import data from matlab and reformat
    contents = sio.loadmat('date_in_str.mat')
    all_people = contents['all_people'] # <class 'numpy.ndarray'> (1,106)
    all_data = contents["all_data"]
    numPeople = all_data.shape[1]

    trans_Ms = []
    #creating transition_matrix for every people
    for i in range(numPeople):
        # p_info = [[time, location, loc_id], ...]
        p_info = np.array(all_data[str(i)])
        loc_id = p_info[:, 2]
        num_loc = len(np.unique(loc_id))
        trans_M = np.zeros((num_loc, num_loc))
        for j in range(len(loc_id) - 1):
            curr_loc = loc_id[j]
            next_loc = loc_id[j+1]
            trans_M[curr_loc, next_loc] = trans_M[curr_loc, next_loc] + 1
        trans_M = softmax(trans_M, axis = 1)
        trans_Ms[i] = trans_M
if __name__ == '__main__':
    transition_matrix()
