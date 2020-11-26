import numpy as np
import scipy.io as sio
import pickle


def load_homeID():
    contents = sio.loadmat('realitymining.mat')
    print("done importing contents from matlab")

    home_ids = np.array(contents['s']['home_ids'])
    home_ids_transpose = home_ids.transpose()

    print(len(home_ids_transpose))

    person_count = 0;
    person = {}
    for i in range(len(home_ids_transpose)):

        home_id = home_ids_transpose[i]
        person[i] = [home_id]
        # print(person)
        person_count += 1

    print(person_count)
    print("done processing data")
    print(person)

    with open('processedhomeID.pickle', 'wb') as handle:
        pickle.dump(person, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("done dumping to pickle")

if __name__ == '__main__':
   load_homeID()
