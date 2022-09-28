v7 = "mG6=S"
s = "1859-1902"
v4 = [0]*9
v5 = [0]*9

for i in range(9):
	if i > 1:
		if i > 3:
			v4[i] = v7[i-4]
		else:
			v4[i] = s[i+5]
	else:
		v4[i] = s[i+2]

for i in range(9):
	v5[i] = chr(int((ord(s[i]) + ord(v4[i])) / 2))
	
print(''.join(v5))
