load('preprocess.mat');
all_people = cell(1,size(locs,2));
counter = 0;
for i = locs
    A = i.locs;
    locArray = cell(size(A,1),2);
    for j = 1: size(A,1)
        locArray(j,1) = {datestr(A(j,1))};
        locArray(j,2) = {A(j,2)};
    end
        
    if mod(counter, 100) == 0
        disp(counter)
    end
    counter = counter + 1;
    all_people(counter) = {locArray};
end
disp(all_people)
