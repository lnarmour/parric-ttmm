# python3

import subprocess
import queue
import threading
import os
import sys
import argparse
import json
from glob import glob

global machines
global tasks
global gflops

global job_cnt
global total_tasks

class Machine:
    def __init__(self, hostname, dns_suffix=None):
        self.tasks = []
        if not dns_suffix:
            dns_suffix = '.cs.colostate.edu'
        self.hostname = '{}{}'.format(hostname, dns_suffix)
    
    def __str__(self):
        return str(self.hostname)


class Command:
    def __init__(self, executable, params, num_runs=7, num_threads=None, permutation=None, loop_parallelized=None, mkl=False, block_size=None, blocks_per_side=None):
        global total_tasks
        self.executable = executable
        self.executable_short_name = executable.split('/')[-1]
        self.params = params
        self.N = params[0]
        # TODO - will need to adjust this for 4D layouts
        self.TS = params[1] if len(params)==4 else None
        self.blocks_per_side= blocks_per_side
        self.block_size=block_size
        self.tiled = True if self.TS else False
        self.num_runs = num_runs
        self.parallel = True if num_threads else False
        self.loop_parallelized = loop_parallelized
        self.num_threads = num_threads
        self.permutation = permutation
        self.mkl = mkl
        self.task_number = total_tasks
        total_tasks += 1

    def __str__(self):
        p_str = ''
        for p in self.params:
            p_str += ' ' + str(p)
        if self.mkl:
            environment_vars = '{}{} '.format('MKL_NUM_THREADS=', self.num_threads) if self.num_threads else ''
        else:
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


    def serialize(self):
        # TODO - haven't fully tested
        ret = {}
        ret["machine"] = str(self.machine)
        ret["command"] = str(self.command)
        ret["task_number"] = self.command.task_number
        ret["permutation"] = self.command.permutation
        ret["N"] = self.command.N
        ret["tiled"] = self.command.tiled
        ret["TS"] = self.command.TS
        ret["blocks_per_side"] = self.command.blocks_per_side
        ret["block_size"] = self.command.block_size
        ret["parallel"] = self.command.parallel
        ret["num_threads"] = self.command.num_threads
        ret["loop_parallelized"] = self.command.loop_parallelized
        ret["error"] = self.error
        ret["error_msg"] = self.error_msg
        ret["times"] = self.times
        return ret

    def __str__(self):
        ret = 'Result\n'
        ret += '  machine: {}\n'.format(self.machine)
        ret += '  command: {}\n'.format(self.command)
        ret += '  task_number: {}\n'.format(self.command.task_number)
        ret += '  host: {}\n'.format(self.machine)
        ret += '  permutation: {}\n'.format(self.command.permutation)
        ret += '  N: {}\n'.format(self.command.N)
        ret += '  tiled: {}\n'.format(self.command.tiled)
        ret += '  TS: {}\n'.format(self.command.TS)
        ret += '  blocks_per_side: {}\n'.format(self.command.blocks_per_side)
        ret += '  block_size: {}\n'.format(self.command.block_size)
        ret += '  parallel: {}\n'.format(self.command.parallel)
        ret += '  num_threads: {}\n'.format(self.command.num_threads)
        ret += '  loop_parallelized: "{}"\n'.format(self.command.loop_parallelized)
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
            results.append(result)
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


def queue_baseline_tasks(filename, path_prefix='.'):
    global hostnames

    with open(filename) as f:
        data = json.load(f)

    # Add tasks to queue
    tasks = queue.Queue()

    for N in data['problem_size']:
        for num_threads in data['mkl_num_threads']:
            tasks.put(Command('{}/SS_MKL'.format(path_prefix), [N], num_threads=num_threads, mkl=True))
            #tasks.put(Command('{}/TS_MKL'.format(path_prefix), [N], num_threads=num_threads, mkl=True))
            tasks.put(Command('{}/TT_MKL'.format(path_prefix), [N], num_threads=num_threads, mkl=True))

    return tasks


def queue_failed_tasks(results_files, path_prefix):
    data = []
    for filename in glob(results_files):
        with open(filename, 'r') as f:
            data += json.load(f)

    # Add tasks to queue
    tasks = queue.Queue()

    data = [x for x in data if len(x['times']) == 0]
    for x in data:
        if x['tiled']:
            if x['parallel']:
                binary = '{}/2D-Parallel/tiled/{}/out/TMM_parallel_{}'.format(path_prefix, x['permutation'],
                                                                              x['loop_parallelized'])
            else:
                binary = '{}/2D-Sequential/tiled/{}/out/TMM'.format(path_prefix, x['permutation'])
        else:
            if x['parallel']:
                binary = '{}/2D-Parallel/nonTiled/{}/out/TMM_parallel_{}'.format(path_prefix, x['permutation'],
                                                                                 x['loop_parallelized'])
            else:
                binary = '{}/2D-Sequential/nonTiled/{}/out/TMM'.format(path_prefix, x['permutation'])

        params = [x['N']]
        if x['TS']:
            params += [x['TS'], x['TS'], x['TS']]

        tasks.put(Command(binary, params, num_threads=x['num_threads'], permutation=x['permutation'],
                loop_parallelized=x['loop_parallelized']))

    return tasks


def queue_tasks(filename, path_prefix='.', N=500, two_d=False, four_d=False, loop_orders_2D=None):
    global hostnames

    with open(filename) as f:
        data = json.load(f)

    # Add tasks to queue
    tasks = queue.Queue()

    if not loop_orders_2D:
        loop_orders_2D = ['ijk', 'ikj', 'jik', 'jki', 'kij', 'kji']
    loop_orders_4D = [outer + inner for outer in ['ijd', 'idj', 'jid', 'jdi', 'dij', 'dji'] for inner in ['kle', 'kel', 'lke', 'lek', 'ekl', 'elk'] ]

    if two_d:
        for permutation in loop_orders_2D:
            binary = '{}/2D-Sequential/nonTiled/{}/out/TMM'.format(path_prefix, permutation)
            tasks.put(Command(binary, [N], permutation=permutation))

            for num_threads in data['omp_num_threads']:
                binaryI = '{}/2D-Parallel/nonTiled/{}/out/TMM_parallel_I'.format(path_prefix, permutation)
                binaryJ = '{}/2D-Parallel/nonTiled/{}/out/TMM_parallel_J'.format(path_prefix, permutation)
                tasks.put(Command(binaryI, [N], num_threads=num_threads, permutation=permutation, loop_parallelized='I'))
                tasks.put(Command(binaryJ, [N], num_threads=num_threads, permutation=permutation, loop_parallelized='J'))

            for TS in data['tile_size']:
                binary = '{}/2D-Sequential/tiled/{}/out/TMM'.format(path_prefix, permutation)
                tasks.put(Command(binary, [N, TS, TS, TS], permutation=permutation))

                for num_threads in data['omp_num_threads']:
                    binaryI = '{}/2D-Parallel/tiled/{}/out/TMM_parallel_I'.format(path_prefix, permutation)
                    binaryJ = '{}/2D-Parallel/tiled/{}/out/TMM_parallel_J'.format(path_prefix, permutation)
                    tasks.put(Command(binaryI, [N, TS, TS, TS], num_threads=num_threads, permutation=permutation, loop_parallelized='I'))
                    tasks.put(Command(binaryJ, [N, TS, TS, TS], num_threads=num_threads, permutation=permutation, loop_parallelized='J'))
    if four_d:
        for permutation in loop_orders_4D:
            binary = '{}/4D-Sequential/tiled/{}/out/BlockTTMM'.format(path_prefix, permutation)

            for TS in data['tile_size']:
                if N < TS:
                    continue
                tasks.put(Command(binary, [N//TS, TS], permutation=permutation, blocks_per_side=N//TS, block_size=TS))
                
        
    return tasks

def main():
    global job_cnt
    global total_tasks
    job_cnt = 0
    total_tasks = 0

    '''Command line options processing.'''
    program_name = os.path.basename(sys.argv[0])

    # parse command line arguments
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('--path-prefix', '--path-prefix', help='String to prepend to >path-prefix>/2D-*/*iled/*/TMM*', default='./workspace/parric-ttmm/ttmm/alphaz_stuff/out')
    parser.add_argument('-f', '--config-file', default=None)
    parser.add_argument('-o', '--out-file', default='./results.json')
    parser.add_argument('-b', '--baseline', default=None)
    parser.add_argument('-2d', '--two-d', default=None)
    parser.add_argument('-4d', '--four-d', default=None)
    parser.add_argument('-lo2d', '--loop-orders-2D', default=None, nargs='+') # loop order 2D
    parser.add_argument('-ffailed', '--failed-tasks', default=None)
    
    args = vars(parser.parse_args())


    with open(args['config_file']) as f:
        data = json.load(f)

    init_machines(data['hostname'])

    if args['baseline']:
        tasks = queue_baseline_tasks(args['config_file'], args['path_prefix'])

        results = []

        if os.getenv("COLLECT"):
            run_workers(machines, tasks, results)
        else:
            for t in list(tasks.queue):
                print(t)

        # print results

        all_results = [r.serialize() for r in results]
        print('gathered {} results'.format(len(all_results)))

        # TODO - json dump all_results to file
        with open('results/baseline.mkl.json', 'w') as outfile:
            json.dump(all_results, outfile, indent=2)

    else:
        for N in data['problem_size']:
            if args['failed_tasks']:
                tasks = queue_failed_tasks(args['failed_tasks'], args['path_prefix'])
            else:
                tasks = queue_tasks(args['config_file'], args['path_prefix'], N, two_d=args['two_d'], four_d=args['four_d'], loop_orders_2D=args['loop_orders_2D'])

            print('Queued {} tasks.'.format(total_tasks))
            results = []

            if os.getenv("COLLECT"):
                run_workers(machines, tasks, results)
            else:
                for t in list(tasks.queue):
                    print(t)

            # print results
            all_results = [r.serialize() for r in results]

            with open('{}_{}.json'.format( args['out_file'], N), 'w') as outfile:
                json.dump(all_results, outfile, indent=2)

            if args['failed_tasks']:
                break

    print('...done.')


if __name__ == '__main__':
    sys.exit(main())










