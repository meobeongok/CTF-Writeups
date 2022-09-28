#!/bin/sh

echo "Nhap n: "
read n
sum=0 
while [ $n -ge 10 ]; do
	echo "Vui long nhap so nho hon 10"
	read n
done 

while [ $n -ne 0 ]; do
	sum=$(($sum+$n))
	n=$(($n-1))
done
echo "Ket qua: $sum"


exit 0 
