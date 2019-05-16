echo 'unbuffer python3 commander.py -N 500 --parent-center 50 50 50 --parent-size 100 -i 2 --partitions 2 2 -k 2 1 --path-prefix ./workspace/parric-ttmm/ttmm/ikj/out | tee -a ~/workspace/parric-ttmm/results/experiment-test.log'
echo ''

unbuffer \
python3 commander.py \
-N 500 \
--parent-center 50 50 50 \
--parent-size 100 \
-i 2 \
--partitions 2 2 \
-k 2 1 \
--path-prefix ./workspace/parric-ttmm/ttmm/ikj/out \
| tee -a ~/workspace/parric-ttmm/results/experiment-test.log
