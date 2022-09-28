#!/bin/sh
echo "Nhap ho va ten: "
read hoten
echo "Nhap mssv: "
read mssv

while [ "$mssv" != "20521859" ]; do
	echo "MSSV khong khop vui long nhap lai: "
	read mssv
done
echo "Ho va ten la: $hoten"
echo "MSSV: $mssv"
exit 0

