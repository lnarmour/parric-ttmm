echo 'unbuffer python3 commander.py -N 8000 -i 4 --partitions 4 2 2 2 -k 3 3 3 1 --path-prefix ./workspace/parric-ttmm/ttmm/ikj/out | tee -a ~/workspace/parric-ttmm/results/experiment-1.log'
echo ''

unbuffer \
python3 commander.py \
-N 8000 \
-i 4 \
--partitions 4 2 2 2 \
-k 3 3 3 1 \
--path-prefix ./workspace/parric-ttmm/ttmm/ikj/out \
| tee -a ~/workspace/parric-ttmm/results/experiment-1.log
