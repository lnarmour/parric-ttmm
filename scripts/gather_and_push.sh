for order in IJK IKJ JIK JKI KIJ KJI; do for index in I J; do bash experiment-${order}-${index}.sh; done; done;

git add ../results/*icc.log
git commit -m "autosaving icc results"
git push origin icc-data

echo 'donzo'
