datapoints=50000
shopt -s nullglob
numfiles=(./Dataset50000/*)
numfiles=${#numfiles[@]}
# echo $numfiles
range=datapoints+numfiles
g++ -o main main.cpp
start=`date +%s%N`
for ((i=$numfiles+1;i<=$range;i++)); do
    ./main $i $datapoints
done
end=`date +%s%N`
echo Execution time was `expr $end - $start` nanoseconds.