echo 'unbuffer python3 commander.py -N 5000 -i 5 --partitions 4 4 4 4 4 -k 16 4 2 2 1 --path-prefix ./workspace/parric-ttmm/ttmm/ikj/out --rectangle | tee -a ~/workspace/parric-ttmm/results/experiment-20180806.log'
echo ''

unbuffer \
python3 commander.py \
-N 5000 \
-i 5 \
--partitions 4 4 4 4 4 \
-k 16 4 2 2 1 \
--path-prefix ./workspace/parric-ttmm/ttmm/ikj/out \
--rectangle 1 \
| tee -a ~/workspace/parric-ttmm/results/experiment-20180806.log
