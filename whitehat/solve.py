v6 = "Vjjp`Nf|roqSua}Ow}aKg%H{q{wpxpxE~mLTX"
s =[0]*37

for i in range(0,37):
	s[i] =chr(int((i+1)^ord(v6[i])))
	
print(''.join(s))
