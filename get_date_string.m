[locs_raw, locs_ids] = loadData();

all_people = cell(1,size(locs_raw,2));

for i = 1:size(locs_raw,2)
    time_and_loc = cell2mat(locs_raw(i));
    if size(time_and_loc,2) == 0
        continue
    end
    
    num_timestamps = size(time_and_loc,1);
    rowDist = ones(num_timestamps,1);
    
    locArray = mat2cell(time_and_loc(:,2),rowDist);
    idArray = mat2cell(cell2mat(locs_ids(i)),rowDist);
    
    timeArray = cell(size(time_and_loc,1),1);
    for j = 1: size(time_and_loc,1)
        timeArray(j,1) = {datestr(time_and_loc(j,1))};
    end
    
    person = cat(2,timeArray,locArray,idArray);
    all_people(1,i) = {person};
    disp(i)
end
disp(all_people)
save('date_in_str.mat','all_people')

function [locs_raw, locs_ids] = loadData()
    realitymining = load('realitymining.mat');
    S = squeeze(struct2cell(realitymining.s));
    locs_raw = S(6,:);  %locs is 1 x 106
    locs_ids = S(8,:);  %loc_ids is 1 x 106
    disp('done loading data')
end
