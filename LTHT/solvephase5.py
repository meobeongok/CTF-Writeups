array = "maduiersnfotvbyl"
res = "flyers"

for i in range(len(res)):
	for j in range(len(array)):
		if(res[i]==array[j]):
			for k in range(65,100):
				if((k&0xf)==j):
					print(chr(k))
					break
			break
	
