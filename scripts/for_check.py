import random
import sys
import os
import argparse

def main():
    '''Command line options processing.'''
    program_name = os.path.basename(sys.argv[0])

    # parse command line arguments
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('-N', '--matrix-size', help='Length of matrix.', default=1000)

    args = vars(parser.parse_args())

    N = int(args['matrix_size'])
    
    
    random.seed(1)
    
    for m in range(2):
        for i in range(N,0,-1):
            print(random.gauss(0,1) * 10000)
            for z in range(i-1):
                print(random.gauss(0,1) * 10000)


if __name__ == '__main__':
    sys.exit(main())

