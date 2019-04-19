
rm -rf temp_data

echo "MKL_NUM_THREADS=${MKL_NUM_THREADS}"
echo ''
echo "SS MKL for N=${N}"
for i in {1..5};
do
	MKL_NUM_THREADS=${MKL_NUM_THREADS} ./SS_MKL $N >> temp_data
done;
python3 calc_time.py

rm -rf temp_data
echo ''
echo "TT MKL (using SS with both bottom half of zeros) for N=${N}"
for i in {1..5};
do
  MKL_NUM_THREADS=${MKL_NUM_THREADS} ./TT_MKL $N >> temp_data
done;
python3 calc_time.py

rm -rf temp_data
echo ''
echo "TS MKL for N=${N}"
for i in {1..5};
do
  MKL_NUM_THREADS=${MKL_NUM_THREADS} ./TS_MKL $N >> temp_data
done;
python3 calc_time.py

rm -rf temp_data
