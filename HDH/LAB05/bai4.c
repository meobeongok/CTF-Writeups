#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

int x1 = 6;
int x2 = 5;
int x3 = 4;
int x4 = 3;
int x5 = 2;
int x6 = 1;
int w, v, z, y, x;
int ans = 0;

sem_t p1_5, p1_6, p2_3, p2_4, p3_5, p4_6, p5_7, p6_7;

void* process1()
{
	w = x1 * x2;
	printf("w = %d\n", w);
	sem_post(&p1_5);
	sem_post(&p1_6);
	sleep(1);
}
void* process2()
{
	v = x3 * x4;
	printf("v = %d\n", v);
	sem_post(&p2_3);
	sem_post(&p2_4);
	sleep(1);
}
void* process3()
{
	sem_wait(&p2_3);
	printf("y = %d\n", y);
	y = v * x5;
	sem_post(&p3_5);
	sleep(1);
}
void *process4()
{
	sem_wait(&p2_4);
	printf("z = %d\n", z);
	z = v * x6;
	sem_post(&p4_6);
	sleep(1);
}
void *process5()
{
	sem_wait(&p1_5);
	sem_wait(&p3_5);
	y = w * y;
	printf("y = %d\n", y);
	sem_post(&p5_7);
	sleep(1);
}
void *process6()
{
	sem_wait(&p1_6);
	sem_wait(&p4_6);
	z = w * z;
	printf("z = %d\n", z);
	sem_post(&p6_7);
	sleep(1);
}
void *process7()
{
	sem_wait(&p5_7);
	sem_wait(&p6_7);
	ans = y + z;
	printf("ans = %d\n", ans);
	sleep(1);
}
void main()
{
	sem_init(&p1_5, 0, 1);
	sem_init(&p1_6, 0, 0);
	sem_init(&p2_3, 0, 0);
	sem_init(&p2_4, 0, 0);
	sem_init(&p3_5, 0, 0);
	sem_init(&p4_6, 0, 0);
	sem_init(&p5_7, 0, 0);
	sem_init(&p6_7, 0, 0);
	pthread_t p1, p2, p3, p4, p5, p6, p7;
	pthread_create(&p1, NULL, &process1, NULL);
	pthread_create(&p2, NULL, &process2, NULL);
	pthread_create(&p3, NULL, &process3, NULL);
	pthread_create(&p4, NULL, &process4, NULL);
	pthread_create(&p5, NULL, &process5, NULL);
	pthread_create(&p6, NULL, &process6, NULL);
	pthread_create(&p7, NULL, &process7, NULL);
	while(1){};
}

