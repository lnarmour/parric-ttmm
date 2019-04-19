import sys
import numpy as np

def discard_extremes(values):
    return sorted(values)[1:-1]

def average(values):
    return sum(values) / len(values)

def main():
    times = []
    try:
        data = open('temp_data', 'r')
        for line in data:
            t = float(line.split(" ")[3])
            times.append(t)
    except:
        pass
    times = discard_extremes(times)
    time = average(times)
    print('{:.3f} +/- {:.3} sec.'.format(time, np.std(times)))
    

if __name__ == '__main__':
    sys.exit(main())

