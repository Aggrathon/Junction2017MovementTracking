
import os

def gen(file):
    def gener():
        with open(file) as f:
            for l in f.readlines():
                split = l[:-1].split(',')
                yield split[2], float(split[0]), float(split[3]), float(split[4]), float(split[5])
    return gener
        

def combine(generator, names, file):
    data = []
    pos = {n:i for i, n in enumerate(names)}
    num = 0.0
    post = [None for _ in names]
    times = 0
    for name, time, x, y, z in generator():
        num += 1
        times += time
        post[pos[name]] = [x, y, z]
        fin = True
        for p in post:
            if p is None:
                fin = False
                break
        if fin:
            line = [times/num]
            times = 0
            num = 0
            for p in post:
                for o in p:
                    line.append(o)
            post = [None for _ in names]
            data.append(line)
    with open(file, 'w') as f:
        f.write('time,'+','.join(n+'/x,'+n+'/y,'+n+'/z,' for n in names)+'\n')
        for d in data:
            f.write(','.join(map(str, d))+'\n')

for file in os.listdir('data'):
    if 'csv' in file and '_' in file and 'fix' not in file:
        combine(
            gen('data/'+file),
            ['174630000602/Meas/Acc/13', '174630000602/Meas/Gyro/13', '174630000495/Meas/Acc/13', '174630000495/Meas/Gyro/13'],
            'data/'+file[:-4]+'_fix.csv')