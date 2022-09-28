#include<stdio.h>

typedef struct {
short a[4];
char b;
int c;  } str1;

int func(int i, int val) {
	str1 s;
	s.c = 1;
	s.a[i] = val;
	return s.c;  }


int main(){
    func(6,2);
    return 0;
}
