import csv
import pickle
from datetime import datetime
import numpy as np

def import_data():
    """
    import time & location data into a dictionary called data
    """
    data = {}
    all_locations = set()
    datetime_format = '%Y-%m-%d %H:%M:%S'
    with open('Barnsdall_2020_03_02_full.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            time = datetime.strptime(row['Location_at'], datetime_format)
            location = (row['Latitude'], row['Longitude'])
            all_locations.add(location)
            if row['Ipv_4'] not in data:
                data[row['Ipv_4']] = [[time, location]]
            else:
                data[row['Ipv_4']].append([time, location])
    print("    ---- done importing data")
    return [data, all_locations]

def preprocess(all_data):
    """
    get rid of people who have less than 75% of average data points
    return dict = {p_id: {hour: (lat, long), ...}, ...}
    """
    tot = 0
    for person in all_data.values():
        tot += len(person)
    avg = tot/len(all_data)
    threshold = avg * 0.75
    new_dict = {}
    for p_id, p_info in all_data.items():
        if len(p_info) >= threshold:
            p_info = np.vstack(p_info)
            p_info = p_info[p_info[:,0].argsort()]
            p_info = keep_longest_duration(p_info)
            new_dict[p_id] = p_info
    return new_dict

def keep_longest_duration(p_info):
    """
    for each hour, only keep the location that the person was at for the longest duration
    param: p_info = np_array([['time','lat','long'],...])
    return: condensed = dict = {hour: (lat, long)}
    """
    max_dur = {}
    condensed = {}
    for i in range(len(p_info) - 1):
        hour = p_info[i][0].replace(minute=0, second=0)
        duration = p_info[i + 1][0] - p_info[i][0]
        if (hour not in max_dur) or (hour in max_dur and duration > max_dur[hour][0]):
            max_dur[hour] = [duration, p_info[i]]
    last_data = p_info[-1][0].replace(minute=0, second=0)
    if last_data not in max_dur:
        max_dur[last_data] = [0,p_info[-1]]
    for hour, data in max_dur.items():
        condensed[hour] = data[1][1]  #"{hour: (lat, long)}"
    return condensed

def main():
    out = import_data()
    processed = preprocess(out[0])
    processed["all_locations"] = list(out[1])

    with open('barnsdall_processed_data.pickle', 'wb') as handle:
        pickle.dump(processed, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()
