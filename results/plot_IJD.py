import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


class Result:
    def __init__(self, N, t1, time):
        self.N = N
        self.t1 = t1
        sideLen=N*t1
        self.gflops = sideLen*sideLen*sideLen*(1.0/6.0)*(10**-9)
        self.time = time

    def __str__(self):
        return 'N={}, T=({}), time={}'.format(self.N, self.t1, self.time)

    def __hash__(self):
        return hash('{}-{}'.format(self.N, self.t1))

    def __eq__(self, other):
        if (self.N != other.N) or (self.t1 != other.t1):
            return False
        else:
            return True
    def gflops_s(self):
        return self.gflops/self.time


def load_results(args):
    # parse raw results from file
    file_name = args['file_path']
    f=open(file_name,"r")
    return get_results_from_file(f)

def get_results_from_file(f):
    results = []
    for line in f:
        if not line.startswith('Result'):
            continue
        line = line.replace(' ','')
        pcs = line.split(':')
        N = int(pcs[1].split('=')[1])
        TS = pcs[2].replace('(','').replace(')','').split(',')[0]
        ts1= int(TS)
        time = float(pcs[3].split('s')[0])
        results.append(Result(N, ts1, time))
    return results


def avg_results(all_results):
    results = {}
    for r in all_results:
        if r not in results:
            results[r] =r
            results[r].time=[results[r].time]
        else:
            results[r].time.append(r.time) 

    for r in results:
        times = np.sort(results[r].time)
        avg = np.mean(times[1:-1])
        results[r].time = avg
    return results


def main(args, all_results):
    results = avg_results(all_results)
    points = {}
    for r in results:
        time = results[r]
        if r.N not in points:
            points[r.N] = {'TS':[r.t1], 'gfps':[r.gflops/time], 'times':[r.time]}
        else:
            points[r.N]['TS'].append(r.t1)
            points[r.N]['times'].append(r.time)
            points[r.N]['gfps'].append(r.gflops/time)

    '''for N in points:
        print(N, 'typ', type(N))
        print('\t', points[N]['TS'])
        print('\t', points[N]['times'])
        print('\t', points[N]['gfps'])
    '''

    x1, x2 = [], []
    y1, y2 = [], []
    for N in points:
        if N % 500 != 0:
            continue
        x1.append(N)
        max = points[N]['gfps'][0];
        for gfps in points[N]['gfps']:
            if gfps < max:
                continue
            max = gfps
        y1.append(max)
    plt.scatter(x1, y1, label='IJK-I 500->8000')

    for N in points:
        if N % 500 == 0:
            continue
        x2.append(N)
        max = points[N]['gfps'][0];
        for gfps in points[N]['gfps']:
            if gfps < max:
                continue
            max = gfps
        y2.append(max)
    plt.scatter(x2, y2, label='IJK-I 512->8192')


    plt.xlabel('tile size (x,x,x)')
    plt.ylabel('gflops/sec')
    plt.title(args['file_path'])
    plt.legend()
    plt.show()








if __name__ == '__main__':
    program_name = os.path.basename(sys.argv[0])
    # parse command line arguments
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('-f', '--file-path', help='results file path', default='')
    args = vars(parser.parse_args())
    results = load_results(args)
    sys.exit(main(args, results))

