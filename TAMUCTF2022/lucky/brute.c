#include <stdio.h>
#include <stdlib.h>

int main() {
	    long i = 5649426;
    while(1){
	    srand(i);
	    int key0 = rand();
	    int key1 = rand();
	    int key2 = rand();
	    printf("Gia tri key0: %d\n", key0);
	    printf("Gia tri key1: %d\n", key1);
	    printf("Gia tri key2: %d\n", key2);
	    printf("Gia tri seed: %d\n\n", i);
	    if (key0 == 306291429 && key1 == 442612432 && key2 == 110107425){
	    	printf("Seed: %d", i);
	    	exit(0);
	    }
	    else {
	    	i++;
	    }
    }
}

