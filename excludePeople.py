import pandas as pd
import pickle
from datetime import datetime

with open('processed.pickle', 'rb') as handle:
    loc = pickle.load(handle) # {‘person_id’: {time: [location, location_id]}, …}

dict2 = loc.copy()
print("Length before readjusting: ", len(loc))

#count = 0
#for p_id, p_info in dict2.items():
#    count += len(p_info)
#    3191241 locations 95 people

for p_id, p_info in dict2.items():
    print("Person ID:", p_id, len(p_info))
    if (len(p_info) < (3191241 / 95 * 0.75)):
        print("The data does not contain 75%")
        del loc[p_id]
    #for key in p_info:
        #fmt = '%H:%M:%S'
        #d1 = datetime.strptime(key[-8:], fmt)
        #minDiff = (d2 - d1).days * 24 * 60 > 30

print("Length after readjusting: ", len(loc))

with open('processed_t.pickle', 'wb') as handle:
    pickle.dump(loc, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("done dumping to pickle")















