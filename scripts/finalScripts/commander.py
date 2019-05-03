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

global job_cnt

class Machine:
    def __init__(self, hostname, dns_suffix=None):
        self.tasks = []
        if not dns_suffix:
            dns_suffix = '.cs.colostate.edu'
        self.hostname = '{}{}'.format(hostname, dns_suffix)
    
    def __str__(self):
        return str(self.hostname)


class Command:
    def __init__(self, executable, params, num_runs=7, num_threads=None, permutation=None):
        self.executable = executable
        self.executable_short_name = executable.split('/')[-1]
        self.params = params
        self.N = params[0]
        # TODO - will need to adjust this for 4D layouts
        self.TS = params[1] if len(params)==4 else None
        self.tiled = True if self.TS else False
        self.num_runs = num_runs
        self.num_threads = num_threads
        self.permutation = permutation

    def __str__(self):
        p_str = ''
        for p in self.params:
            p_str += ' ' + str(p)
        environment_vars = '{}{} '.format('OMP_NUM_THREADS=', self.num_threads) if self.num_threads else ''
        return environment_vars + str(self.executable) + p_str

    def log(self):
        p_str = ''
        for p in self.params:
            p_str += ' ' + str(p)
        environment_vars = '{}{} '.format('OMP_NUM_THREADS=', self.num_threads) if self.num_threads else ''
        return environment_vars + str(self.executable_short_name) + p_str

    def as_list(self):
        ret = [str(self.executable)]
        for p in self.params:
            ret.append(str(p))
        return ret

    def __hash__(self):
        return (self.executable, tuple(self.params)).__hash__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.executable == other.executable and self.params == other.params

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        # In case a tuple with a command at the end ties the previous results during a sort
        return self.__hash__() < other.__hash__()


class Result:
    def __init__(self, machine, command, times, error=False, error_msg=None):
        self.machine = machine
        self.command = command
        self.times = times
        self.error = error
        self.error_msg = error_msg

    def jsonify(self):
        # TODO - haven't fully tested
        ret = '{'
        ret += '"command":"{}",'.format(self.command)
        ret += '"host":"{}",'.format(self.machine)
        ret += '"permutation":"{}",'.format(self.command.permutation)
        ret += '"N":{},'.format(self.command.N)
        ret += '"tiled":{},'.format(self.command.tiled)
        ret += '"TS":{},'.format(self.command.TS)
        ret += '"error":{},'.format(self.error)
        ret += '"error_msg":"{}",'.format(self.error_msg)
        ret += '"times":{}'.format(self.times)
        ret += '}'
        return ret

    def __str__(self):
        ret = 'Result\n'
        ret += '  command: {}\n'.format(self.command)
        ret += '  host: {}\n'.format(self.machine)
        ret += '  permutation: {}\n'.format(self.command.permutation)
        ret += '  N: {}\n'.format(self.command.N)
        ret += '  tiled: {}\n'.format(self.command.tiled)
        ret += '  TS: {}\n'.format(self.command.TS)
        ret += '  error: {}\n'.format(self.error)
        ret += '  error_msg: {}\n'.format(self.error_msg)
        ret += '  times: {}'.format(self.times)
        return ret


def worker(machine, tasks, results):
    global job_cnt
    while True:
        command = tasks.get()
        if not command:
            break

        command_string = '{} && '.format(str(command)) * (command.num_runs-1)+ str(command)

        # remotely invoke 'command' on 'machine' via ssh
        echo_pipe = subprocess.Popen(['echo', str(command_string)], stdout=subprocess.PIPE)
        ssh_pipe = subprocess.Popen(['ssh', '-T', str(machine.hostname)], stdin=echo_pipe.stdout, stdout=subprocess.PIPE)
        result_bytes = ssh_pipe.stdout.read()
        try:
            arr = result_bytes.decode('utf-8').split('\n')[:-1]  # b'Execution time : 0.062362 sec.'
            k = -1 * command.num_runs
            arr = arr[k:]
            times = [float(s.split(' ')[3]) for s in arr]
            result = Result(machine, command, times)
        except:
            result = Result(machine, command, None, error=True, error_msg=result_bytes)
        finally:
            tasks.task_done()
            if not command in results:
                results[command]=[]
            results[command].append(result)
            print(result)


def run_workers(machines, tasks, results):
    threads = []
    for machine in machines:
        t = threading.Thread(target=worker, args=(machine, tasks, results))
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


def queue_tasks(filename, path_prefix='.'):
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
                binary = '{}/2D-Sequential/nonTiled/{}/out/TMM'.format(path_prefix, permutation)
                tasks.put(Command(binary, [N], permutation=permutation))
                binary = '{}/2D-Sequential/tiled/{}/out/TMM'.format(path_prefix, permutation)
                tasks.put(Command(binary, [N, TS, TS, TS], permutation=permutation))

                for num_threads in data['omp_num_threads']:
                    binaryI = '{}/2D-Parallel/nonTiled/{}/out/TMM_parallel_I'.format(path_prefix, permutation)
                    binaryJ = '{}/2D-Parallel/nonTiled/{}/out/TMM_parallel_J'.format(path_prefix, permutation)
                    tasks.put(Command(binaryI, [N], num_threads=num_threads, permutation=permutation))
                    tasks.put(Command(binaryJ, [N], num_threads=num_threads, permutation=permutation))
                    binaryI = '{}/2D-Parallel/tiled/{}/out/TMM_parallel_I'.format(path_prefix, permutation)
                    binaryJ = '{}/2D-Parallel/tiled/{}/out/TMM_parallel_J'.format(path_prefix, permutation)
                    tasks.put(Command(binaryI, [N, TS, TS, TS], num_threads=num_threads, permutation=permutation))
                    tasks.put(Command(binaryJ, [N, TS, TS, TS], num_threads=num_threads, permutation=permutation))

    return tasks

def main():
    global job_cnt
    job_cnt = 0

    '''Command line options processing.'''
    program_name = os.path.basename(sys.argv[0])

    # parse command line arguments
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('--path-prefix', '--path-prefix', help='String to prepend to >path-prefix>/2D-*/*iled/*/TMM*', default='./workspace/parric-ttmm/ttmm/alphaz_stuff/out')
    parser.add_argument('-f', '--config-file', default=None)
    args = vars(parser.parse_args())

    tasks = queue_tasks(args['config_file'], args['path_prefix'])

    results = {}

    if os.getenv("COLLECT"):
        run_workers(machines, tasks, results)
    else:
        for t in list(tasks.queue):
            print(t)

    # print results
    print('--------------------')
    for k in results:
        print(str(results[k][0].jsonify()))
    print('...done.')


if __name__ == '__main__':
    sys.exit(main())










