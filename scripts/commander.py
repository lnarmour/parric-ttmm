# python3

import subprocess
import queue
import threading
import statistics
import os
import sys
import argparse

global machines
global hostnames
global tasks
global level
global master_cube_N
global gflops

hostnames = [
    'anchovy',
    'barracuda',
    'blowfish',
    'bonito',
    'brill',
    'char',
    'cod',
    'dorado',
    'eel',
    'flounder',
    'grouper',
    'halibut',
    'herring',
    'mackerel',
    'marlin',
    'perch',
    'pollock',
    'sardine',
    'shark',
    'sole',
    'swordfish',
    'tarpon',
    'turbot',
    'tuna',
    'wahoo'
]


def partition(parent, segments):
    if not (isinstance(parent, Cube)or isinstance(parent, Rectangle)):
        raise ValueError('passed non-Cube object as parent. parent must be a Cube')
    if segments < 1:
        raise ValueError('segments must be 1 or greater')

    children = []
    (x_p, y_p, z_p) = parent.c
    if isinstance(parent, Cube):
        (x_p, y_p, z_p) = (x_p-parent.l//2, y_p-parent.l//2, z_p-parent.l//2) #convert center into point at bottom left
        step = int(parent.l / segments)  # if segments is 4 and parent.l is N, then step = N/4
        for x in range(0, segments): 
            x_c = x_p + x*step + step // 2
            for y in range(0, segments):
                y_c = y_p + y*step + step // 2
                for z in range(0, segments):
                    z_c = z_p + z*step + step // 2
                    child = Cube(center=(x_c,y_c,z_c), side_length=step)
                    children.append(child)
    if isinstance(parent, Rectangle):
        (x_p, y_p, z_p) = (x_p-parent.ls[0]//2, y_p-parent.ls[1]//2, z_p-parent.ls[2]//2) #convert center into point at bottom left
        steps = tuple([int(l / segments) for l in parent.ls])  # if segments is 4 and parent.l is N, then step = N/4
        for x in range(0, segments): 
            x_c = x_p + x*steps[0] + steps[0] // 2
            for y in range(0, segments):
                y_c = y_p + y*steps[1] + steps[1] // 2
                for z in range(0, segments):
                    z_c = z_p + z*steps[2] + steps[2] // 2
                    child = Rectangle((x_c,y_c,z_c), steps)
                    children.append(child)
    
    return children


class Cube:
    
    def __init__(self, center=None, side_length=2):
        (x, y, z) = center
        if not (isinstance(x, int) and isinstance(y, int) and isinstance(z, int)):
            raise ValueError('origin must be integer tuple')
        if not isinstance(side_length, int):
            raise ValueError('side_length be an integer')
        self.c = center
        self.l = side_length

    def __str__(self):
        return str({'length': self.l, 'center': self.c})

    def center(self):
        return self.c

class Rectangle:
    
    def __init__(self, center, steps):
        (x, y, z) = center
        if not (isinstance(x, int) and isinstance(y, int) and isinstance(z, int)):
            raise ValueError('origin must be integer tuple')
        self.c = center
        self.ls= steps

    def __str__(self):
        return str({'length':self.ls, 'center': self.c})

    def center(self):
        return self.c

class Machine:
    def __init__(self, hostname):
        self.tasks = []
        self.hostname = hostname
        self.cores = 1 # self.calc_cores()
    
    def __str__(self):
        return str(self.hostname)

    def calc_cores(self):
        # $ lscpu | grep -i socket
        # Core(s) per socket:  8
        # Socket(s):           1
        cores_per_socket_pipe = subprocess.Popen(['echo', 'lscpu | grep -i "per socket"'] , stdout=subprocess.PIPE)
        cps_str = subprocess.Popen(['ssh', '-T', self.hostname], stdin=cores_per_socket_pipe.stdout, stdout=subprocess.PIPE).stdout.read()

        sockets_pipe = subprocess.Popen(['echo', 'lscpu | grep "Socket"'] , stdout=subprocess.PIPE)
        socks_str = subprocess.Popen(['ssh', '-T', self.hostname], stdin=sockets_pipe.stdout, stdout=subprocess.PIPE).stdout.read()

        cores_per_socket = int(cps_str.decode('utf-8').split(':')[1].replace(' ', ''))
        sockets = int(socks_str.decode('utf-8').split(':')[1].replace(' ', ''))

        return cores_per_socket * sockets


class Command:
    def __init__(self, executable, params):
        self.executable = executable
        self.params = params

    def __str__(self):
        p_str = ''
        for p in self.params:
            p_str += ' ' + str(p)
        return str(self.executable) + p_str

    def as_list(self):
        ret = [str(self.executable)]
        for p in self.params:
            ret.append(str(p))
        return ret
    
    def __hash__(self):
        return (self.executable, tuple(self.params)).__hash__()
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.executable==other.executable and self.params==other.params
    
    def __ne__(self, other):
        return not self==other

    def __lt__(self, other):
        #In case a tuple with a command at the end ties the previous results during a sort
        return self.__hash__() < other.__hash__()


class Result:
    def __init__(self, machine, core, command, time, level, parent):
        self.machine = machine
        self.core = core
        self.command = command
        self.time = time
        self.level = level
        self.parent = parent

    def __str__(self):
        ret = 'Result [' +  str(self.machine) + '-'
        if self.core >= 0:
            ret += str(self.core) + ']'
        if self.level >= 0:
            ret += ' : level-' + str(self.level)
        if isinstance(self.parent, Cube) or isinstance(self.parent, Rectangle):
            ret += ' : parent' + str(self.parent.c)
        else:
            ret += ' : N={}'.format(self.parent)
        ret += ' : ' + str(tuple(self.command.params[1:])) + ' : ' + str(self.time) + ' seconds'
        return ret

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time


def init_machines():
    global machines
    global hostnames
    machines = []
    for h in hostnames:
        print('Creating','Machine(\''+str(h)+'\')...', end='')
        machines.append(Machine(h))
        print('done.')


def worker2(machine, tasks, results):
    #global tasks
    #global level
    while True:
        command = tasks.get()
        if not command:
            break

        # remotely invoke 'command' on 'machine' via ssh
        echo_pipe = subprocess.Popen(['echo', str(command)], stdout=subprocess.PIPE)
        ssh_pipe = subprocess.Popen(['ssh', '-T', str(machine.hostname)], stdin=echo_pipe.stdout, stdout=subprocess.PIPE)
        result_bytes = ssh_pipe.stdout.read()  # b'Execution time : 0.062362 sec.\n'
        #print('@@@@@@>', ['echo', str(command)], '<@@@@')
        #print('======>', ['ssh', '-T', str(machine.hostname)], '<====')
        #print('------>', result_bytes.decode('utf-8')) #.split('\n')[-1])
        #print('######>', result_bytes.decode('utf-8').split('\n')[-1])
        time = float(result_bytes.decode('utf-8').split('\n')[-2].split(' ')[3])
        result = Result(machine, -1, command, time, -1, command.params[0])
        if not command in results:
            results[command]=[]
        results[command].append(result)

        print(str(result))

        tasks.task_done()


def worker(machine, core, tasks, level, results, parent):
    #global tasks
    #global level
    while True:
        command = tasks.get()
        if not command:
            break

        # remotely invoke 'command' on 'machine' via ssh
        echo_pipe = subprocess.Popen(['echo', str(command)], stdout=subprocess.PIPE)
        ssh_pipe = subprocess.Popen(['ssh', '-T', str(machine.hostname)], stdin=echo_pipe.stdout, stdout=subprocess.PIPE)
        result_bytes = ssh_pipe.stdout.read()  # b'Execution time : 0.062362 sec.\n'
        #print('------>', result_bytes.decode('utf-8'))
        time = float(result_bytes.decode('utf-8').split(' ')[3])
        result = Result(machine, core, command, time, level, parent)
        if not command in results:
            results[command]=[]
        results[command].append(result)

        print(str(result))

        tasks.task_done()


def run_workers2(machines, tasks, results):

    threads = []
    for machine in machines:
        for i in range(0, machine.cores):
            t = threading.Thread(target=worker2, args=(machine, tasks, results))
            t.start()
            threads.append(t)
    tasks.join()

    for t in threads:
        tasks.put(None)

    for t in threads:
        t.join()


def run_workers(machines, tasks, level, results, parent):
    #global results
    #global machines
    #global tasks

    threads = []
    for machine in machines:
        for i in range(0, machine.cores):
            t = threading.Thread(target=worker, args=(machine, i, tasks, level, results, parent))
            t.start()
            threads.append(t)
    tasks.join()

    for t in threads:
        tasks.put(None)

    for t in threads:
        t.join()


# python3 commander.py -N 5000 --parent-center 500 500 500 --parent-size 1000 -i 4 --partitions 4 4 4 4 -k 16 4 2 2 --path-prefix ./workspace/parric-ttmm/ttmm/ikj/out
def main():
    '''Command line options processing.'''
    program_name = os.path.basename(sys.argv[0])

    # parse command line arguments
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('-N', '--matrix-size', help='Length of matrix.', default=1000)
    parser.add_argument('--path-prefix', '--path-prefix', help='Path to directory containing TMM executable file', default='./workspace/parric-ttmm/ttmm/alphaz_stuff/out')
    parser.add_argument('-k', '--keep', help='Comma-delimited list of number of results to keep at each iteration', nargs='+')
    parser.add_argument('--partitions', '--partitions', help='Comma-delimited list of number of partitions to divide each dimension in at each iteration. For example, [4,2] divides the parent cube into 64 cubes (4^3) on the first iteration, and divides each of those 64 cubes into 8 cubes (2^3) for the second iteration.', nargs='+')
    parser.add_argument('--parent-center', '--parent-center', help='Comma-delimted list of initial parent center.', nargs='+')
    parser.add_argument('--parent-size', '--parent-size', help='Size of initial parent.')
    parser.add_argument('--rectangle')
    parser.add_argument('-f', '--config-file', default=None)

    parser.add_argument('-i', '--iterations', help='Number of times to recurse down into smaller cubes.', default=3)

    args = vars(parser.parse_args())

    N = int(args['matrix_size'])
    path_prefix = args['path_prefix']
    keep = [int(i) for i in args['keep']] if args['keep'] else []
    partitions = [int(i) for i in args['partitions']] if args['partitions'] else []
    iterations = int(args['iterations'])

    parent_center = tuple([int(i) for i in args['parent_center']]) if args['parent_center'] else None
    parent_size = int(args['parent_size']) if args['parent_size'] else None
    if (parent_center and not parent_size) or (not parent_center and parent_size):
        print('Must specify niether OR both --parent-center and --parent-size.')
        print(parser.print_help())
        sys.exit()
    if parent_center and parent_size:
        parent = Cube(parent_center, parent_size)
    else:
        parent = None
    
    args_log = {'N':N, 'path_prefix':path_prefix, 'keep':keep, 'partitions':partitions, 'parent_center':parent_center, 'parent_size':parent_size, 'iterations':iterations}
    print('args', ':', args_log, end='\n\n')



    if args['rectangle']:
        parent = Rectangle( ( 500, 32, 3000), ( 1000, 64, 2000) )
        
    if args['config_file']:
        return main_helper2(config_filename=args['config_file'], path_prefix=path_prefix)
    else:
        return main_helper(N=N, partitions=partitions, path_prefix=path_prefix, keep=keep, iterations=iterations, parent=parent)



def main_helper2(config_filename='./config', path_prefix=''):

    #load tasks from file
    N = []
    TS = []
    try:
        config = open(config_filename, 'r')
        for line in config:
            pieces = line.split(':')
            if pieces[0] == 'N':
                N.append(int(pieces[1]))
            elif pieces[0] == 'TS':
                #pieces[1] = 1,2,3
                ts = pieces[1].split(',')
                TS.append((int(ts[0]),int(ts[1]),int(ts[2])))
        #print(N)
        #print(TS)
    except:
        print('oh well')

    init_machines()
    # Add tasks to queue
    tasks = queue.Queue()
    print('\nCreating tasks from config file...')
    for n in N:
        for ts in TS:
            (ts1, ts2, ts3) = ts
            for i in range(5):
                tasks.put(Command('{}/TMM'.format(path_prefix), [n, ts1, ts2, ts3]))
                #print(Command('{}/TMM'.format(path_prefix), [n, ts1, ts2, ts3]))

    results = {}
    run_workers2(machines, tasks, results)

    # print results
    for result in results:
        print(result)
    print('...done.')


# main_helper(N=5000, 
#    partitions=[4,4,4,4],
#    path_prefix='./workspace/parric-ttmm/ttmm/ikj/out',
#    keep=[16,4,2,2], 
#    iterations=4, 
#    parent=c.Cube((500,500,500),1000)
#    )
def main_helper(N=1000, partitions=[], path_prefix='./workspace/parric-ttmm/ttmm/alphaz_stuff/out', keep=[], iterations=3, parent=None):
    global machines
    global master_cube_N
    global gflops
    master_cube_N = N
    init_machines()
    gflops = N*N*N*(1.0/3.0)*(10**-9)

    if not parent:
        parent = Cube((N//2, N//2, N//2), N)

    tasks = queue.Queue()

    if not partitions:
        partitions = [2] * iterations
    if not keep:
        keep = [1] * iterations

    main_rec(0, parent, partitions, path_prefix, keep, iterations)


def main_rec(level, parent, partitions, path_prefix, keep, iterations, best_time=None):
    global master_cube_N
    global gflops
    
    if level >= iterations:
        print('\nOPTIMAL',':', parent.center(), best_time, 'seconds', ':', gflops/best_time, 'GFlops/sec')
        return
    
    results={}
    # Add tasks to queue
    tasks = queue.Queue()
    print('\nCreating tasks for parent', parent.c,'...')
    for child in partition(parent, partitions[level]):
        (ts1, ts2, ts3) = child.center()
        for i in range(5):
            tasks.put(Command('{}/TMM'.format(path_prefix), [master_cube_N, ts1, ts2, ts3]))
    run_workers(machines, tasks, level, results, parent)
    print('...done.')
    
    # choose best results for next iteration, i.e. next set of parents
    sorted_results=[(results[command], command) for command in results]
    sorted_results=sorted([ ( statistics.mean([r.time for r in sr[0]]), sr[1]) for sr in sorted_results]) 
    print('\nChoosing best', keep[level], 'results...')
    for r in sorted_results[:keep[level]]:
        print('Selected :', tuple(r[1].params[1:]), str(r[0]), 'seconds')
        origin = tuple(r[1].params[1:]) # command.params = [1000, 250, 250, 750]
    print('...done.')

    for r in sorted_results[:keep[level]]: 
        if isinstance(parent, Cube):
            main_rec(level+1, Cube(tuple(r[1].params[1:]), parent.l//partitions[level]), partitions, path_prefix, keep, iterations, best_time=r[0])
        elif isinstance(parent, Rectangle):
            pl = partitions[level]
            main_rec(level+1, Rectangle(tuple(r[1].params[1:]), (parent.ls[0]//pl, parent.ls[1]//pl, parent.ls[2]//pl)), partitions, path_prefix, keep, iterations, best_time=r[0])


if __name__ == '__main__':
    sys.exit(main())










 
