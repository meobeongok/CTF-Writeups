#!/bin/sh
echo "Nhap vao chuoi de kiem tra: "
read input

for a in $(ls *.txt)
do
	if grep $input $a;
	then echo "Ton tai chuoi trong file $a"
	else
	echo "Khong co chuoi"
	fi
done


exit 0 
