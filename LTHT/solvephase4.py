def func4(a1, a2, a3):
  v4 = (a3 - a2) / 2 + a2;
  if ( v4 > a1 ):
    return func4(a1, a2, v4 - 1) + v4
  if ( v4 >= a1 ):
    return (a3 - a2) / 2 + a2
  return func4(a1, v4 + 1, a3) + v4
  
  
for i in range(0,14):
	if(func4(i,0,14)==18):
		print(i)
