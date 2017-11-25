"""
    Convert all raw logs to csvs
"""
import os

def parse_json(filename):
    data = []
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            start = line.find(':')+1
            end = line.find(' ', start)
            split = line[start:end].split(':')
            time = int(split[-2])*60 + float(split[-1].replace(',', '.'))
            start = line.find('"x":', start+2)+5
            end = line.find(',', start)
            x = float(line[start:end].replace(',', ','))
            start = line.find('"y":', end+2)+5
            end = line.find(',', start)
            y = float(line[start:end].replace(',', ','))
            start = line.find('"z":', end+2)+5
            end = line.find('}', start)
            z = float(line[start:end].replace(',', ','))
            data.append((time, x, y, z))
    with open(filename[:filename.rfind('.')]+'.csv', "w") as file:
        file.write("time,x,y,z\n")
        for t, x, y, z in data:
            file.write('%f,%f,%f,%f\n'%(t,x,y,z)) 

if __name__ == "__main__":
    for file in os.listdir('data'):
        parse_json('data/'+file)