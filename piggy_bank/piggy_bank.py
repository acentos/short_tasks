#!/usr/bin/env python

import os
import csv
import datetime

#### You purpose ####
purpose = 150000
#####################
csv_file = "{0}_percentage.csv".format(purpose)
print("Money box, goal: {0}".format(purpose))
laid = input("Insert new arrival: ")
fieldnames = ['date', 'laid', 'percent', 'balance', 'done']
current_date = datetime.date.today().strftime("%B %d, %Y")
data = {}
anbalance = int(laid)

def percentage(purpose, laid):
    return '%.3f'%(100 * float(laid) / float(purpose))


if not os.path.isfile(csv_file):
    with open(csv_file, mode='w') as csv_obj:
        writer = csv.DictWriter(csv_obj, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'date': current_date,
            'laid': int(laid),
            'percent': percentage(purpose, int(laid)),
            'balance': int(laid),
            'done': percentage(purpose, int(laid))})
    
    print("{0}: {1}".format(current_date, int(laid)))
else:
    with open(csv_file, mode='r') as csv_obj:
        reader = csv.DictReader(csv_obj)
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
        
    anlaidsum = sum([int(dblaid) for dblaid in data['laid']]) + int(laid)
    
    print("{0}: {1}".format(current_date, anlaidsum))
    
    with open(csv_file, mode='a') as csv_obj:
        writer = csv.DictWriter(csv_obj, delimiter=",", fieldnames=fieldnames)
        writer.writerow({
            'date': current_date,
            'laid': int(laid),
            'percent': percentage(purpose, laid),
            'balance': anlaidsum,
            'done': percentage(purpose, anlaidsum)})

    if int(anlaidsum) >= purpose:
        print("Goal achieved!!!\nTotal: {0}, {1}%".format(
            anlaidsum, percentage(purpose, anlaidsum)))
            
