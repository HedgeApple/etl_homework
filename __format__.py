import sys
import csv

files = sys.argv[1:]
for file in files:
    with open(file) as f:
        reader = csv.reader(f)
        i = 0
        for r in reader:
            if i >= 2:
                break
            print('***************************************************', list(enumerate(r)))
            print(len(r))
            i += 1


indeces = [0,1,19,16,15,17,50,6,8,False,12,11,9,10,135,136,137,138,139,140,141,145,56,129,0,125,'if 47 has a url',24,26]
