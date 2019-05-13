echo 'unbuffer python3 commander.py -N 5000 -i 3 --partitions 6 5 4 -k 32 12 1 --path-prefix ./workspace/parric-ttmm/ttmm/ikj/out | tee -a ~/workspace/parric-ttmm/results/experiment-20180805.log'
echo ''

unbuffer \
python3 commander.py \
-N 5000 \
-i 3 \
--partitions 6 5 4 \
-k 32 12 1 \
--path-prefix ./workspace/parric-ttmm/ttmm/ikj/out \
| tee -a ~/workspace/parric-ttmm/results/experiment-20180805.log
