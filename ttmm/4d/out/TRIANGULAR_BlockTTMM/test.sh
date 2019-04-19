rm -rf temp_data
for i in 1 6;
do
	for j in 1 6;
	do
		echo "OMP=$i,  MKL=$j"
		for k in {1..5};
		do
			OMP_NUM_THREADS=$i MKL_NUM_THREADS=$j ./BlockTTMM $N 144 >> temp_data
		done;
		python3 ../../mkl/calc_time.py
		rm -rf temp_data
	done;
done;
