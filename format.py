import sys
import csv

guide = sys.argv[1]
with open(guide) as g:
    reader = csv.reader(g)
    headers = next(reader)
files = sys.argv[2:]
arr_of_needed_val_i = [0,1,19,16,15,17,50,6,8,'9',12,11,9,10,135,136,137,138,139,140,141,145,56,129,0,125,'26',24,26,83,81,113,114,-1,11,-1,-1,-1,-1,-1,75,-1,-1,105,'44',-1,14,-1,'48',126,'50',104,-1,94,77,-1,80,-1,128,61,59,60,58,66,64,65,63,71,69,70,68,51]
for file in files:
    rows = []
    with open(file) as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            dims = r[127].split('x')
            b1 = int(r[79]) if r[79] != '' else 0
            b2 = int(r[84]) if r[84] != '' else 0
            adjustments = {'9': False,
                            '26': 'No' if r[47] != '' else 'Yes',
                            '44': str(b1 + b2),
                            '48': dims[0] if len(dims) == 2 else '',
                            '50': dims[1] if len(dims) == 2 else ''
                            }
            new_row = []
            for i in arr_of_needed_val_i:
                if i in adjustments:
                    new_row.append(adjustments[i])
                else:
                    new_row.append(r[i])
            rows.append(new_row)
    name = file.split('.')[0]
    with open('{0}_formatted.csv'.format(name), 'w') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(headers)
        writer.writerows(rows)
