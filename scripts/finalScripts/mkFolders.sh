#!/bin/bash

#$1 - folder you want to generate the codes in

first=("d" "i" "j");
second=("e" "k" "l");

if [ -z "$1" ]
then
echo missing directory location argument
else

cd $1;

let count=0;
for((a=0; a<3; a++));
do
    start="${first[$a]}${first[($a+1)%3]}${first[($a+2)%3]}";
    start2="${first[$a]}${first[($a+2)%3]}${first[($a+1)%3]}";

    for((c=0; c<3;c++));
    do
        end="${second[$c]}${second[($c+1)%3]}${second[($c+2)%3]}";
        end2="${second[$c]}${second[($c+2)%3]}${second[($c+1)%3]}";
        mkdir "${start}${end}";
        mkdir "${start}${end2}";
        mkdir "${start2}${end}";
        mkdir "${start2}${end2}";
        count=$((count+4));
    done
done;
#cd ..;

echo Finished making $count folders;
fi