#include<stdio.h>

int main(){
	char s[4];
	for(int i=0;i<90;i++){
		for (int i = 0; i <= 3; ++i )
      			s[i] = rand() % 26 + 97;
		printf(s);
		printf("\n");
	}
}
