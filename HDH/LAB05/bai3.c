#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

static int x = 0;

void* processA()
{
	while (1)
	{
		x = x + 1;
		if (x == 20)
		{
			x = 0;
		}
		printf("Process A: x = %d\n", x);
	}
}
void* processB()
{
	while (1)
	{
		x = x + 1;
		if (x == 20)
		{
			x = 0;
		}
		printf("Process B: x = %d\n", x);
	}
}
void main()
{
	pthread_t pA, pB;
	pthread_create(&pA, NULL, &processA, NULL);
	pthread_create(&pB, NULL, &processB, NULL);
	while (1){};
}

