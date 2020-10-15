# delineo-markov-sketch

get_date_string.m converts the time to string first in matlab using datestr() and formats the data a little nicer.
-- output: all_people: (1x106), all_people[i] = array(array(time,loc,loc_id),...)

preprocess.py
-- STAGE 1: import data from matlab and reformat to dictionary: {person_id:{time:[loc,loc_id],...},...}
-- STAGE 2: get rid of people with less than 75% of average number of data points
-- STAGE 3: get hourly data
