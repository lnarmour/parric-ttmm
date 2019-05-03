# python3

import subprocess
import queue
import threading
import os
import sys
import argparse
import json

global machines
global tasks
global gflops

class Machine:
    def __init__(self, hostname):
        self.tasks = []
        self.hostname = hostname
    
    def __str__(self):
        return str(self.hostname)


class Command:
    def __init__(self, executable, params, num_runs=7, num_threads=None):
        self.executable = executable
        self.params = params
        self.num_runs = num_runs
        self.num_threads = num_threads

    def __str__(self):
        p_str = ''
        for p in self.params:
            p_str += ' ' + str(p)
        environment_vars = '{}{} '.format('OMP_NUM_THREADS=', self.num_threads) if self.num_threads else ''
        return environment_vars + str(self.executable) + p_str

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
        ret = 'Result [' + str(self.time) + ' seconds'
        return ret

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time


def worker(machine, core, tasks, level, results, parent):
    while True:
        command = tasks.get()
        if not command:
            break

        # remotely invoke 'command' on 'machine' via ssh
        echo_pipe = subprocess.Popen(['echo', str(command)], stdout=subprocess.PIPE)
        ssh_pipe = subprocess.Popen(['ssh', '-T', str(machine.hostname)], stdin=echo_pipe.stdout, stdout=subprocess.PIPE)
        result_bytes = ssh_pipe.stdout.read()  # b'Execution time : 0.062362 sec.\n'
        time = float(result_bytes.decode('utf-8').split(' ')[3])
        result = Result(machine, core, command, time, level, parent)
        if not command in results:
            results[command]=[]
        results[command].append(result)

        print(str(result))

        tasks.task_done()


def run_workers(machines, tasks, level, results, parent):
    threads = []
    for machine in machines:
        t = threading.Thread(target=worker, args=(machine, i, tasks, level, results, parent))
        t.start()
        threads.append(t)
    tasks.join()

    for t in threads:
        tasks.put(None)

    for t in threads:
        t.join()


def init_machines(hostnames):
    global machines
    machines = []
    for h in hostnames:
        print('Creating','Machine(\''+str(h)+'\')...', end='')
        machines.append(Machine(h))
        print('done.')


def load_config(filename, path_prefix='.'):
    global hostnames

    with open(filename) as f:
        data = json.load(f)

    init_machines(data['hostname'])

    # Add tasks to queue
    tasks = queue.Queue()
    print('\nCreating tasks from config file...')

    loop_orders_2D = ['ijk', 'ikj', 'jik', 'jki', 'kij', 'kji']
    loop_orders_4D = []

    for N in data['problem_size']:
        for TS in data['tile_size']:
            for permutation in loop_orders_2D:
                binary = '{}/2D-Sequential/nonTiled/{}/TMM'.format(path_prefix, permutation)
                tasks.put(Command(binary, [N]))
                binary = '{}/2D-Sequential/tiled/{}/TMM'.format(path_prefix, permutation)
                tasks.put(Command(binary, [N, TS, TS, TS]))

                for num_threads in range(1, 7):
                    binaryI = '{}/2D-Parallel/nonTiled/{}/TMM_parallel_I'.format(path_prefix, permutation)
                    binaryJ = '{}/2D-Parallel/nonTiled/{}/TMM_parallel_J'.format(path_prefix, permutation)
                    tasks.put(Command(binaryI, [N], num_threads=num_threads))
                    tasks.put(Command(binaryJ, [N], num_threads=num_threads))
                    binaryI = '{}/2D-Parallel/tiled/{}/TMM_parallel_I'.format(path_prefix, permutation)
                    binaryJ = '{}/2D-Parallel/tiled/{}/TMM_parallel_J'.format(path_prefix, permutation)
                    tasks.put(Command(binaryI, [N, TS, TS, TS], num_threads=num_threads))
                    tasks.put(Command(binaryJ, [N, TS, TS, TS], num_threads=num_threads))

    return tasks

def main():
    '''Command line options processing.'''
    program_name = os.path.basename(sys.argv[0])

    # parse command line arguments
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('--path-prefix', '--path-prefix', help='Path to directory containing TMM executable file', default='./workspace/parric-ttmm/ttmm/alphaz_stuff/out')
    parser.add_argument('-f', '--config-file', default=None)
    args = vars(parser.parse_args())

    tasks = load_config(args['config_file'])
    for t in list(tasks.queue):
        print(t)

    results = {}

    #run_workers(machines, tasks, results)

    # print results
    for result in results:
        print(result)
    print('...done.')


if __name__ == '__main__':
    sys.exit(main())










