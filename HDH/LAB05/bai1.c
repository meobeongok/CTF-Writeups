#include<stdio.h>
#include<semaphore.h>
#include<pthread.h>

int sells = 0, products = 0;
sem_t sem; 

void *processA(){
	while(1){
		sem_wait(&sem);
		sells++;
		printf("SELLS = %d\n",sells);
		sleep(2);
	}
}

void *processB(){
	while(1){
		while(products <=sells + 59 + 10){
			products++;
			printf("PRODUCTS = %d\n", products);
		}
		sem_post(&sem);	
		sleep(1);
	}
}

int main(){
	sem_init(&sem, 0, 0);
	pthread_t pA, pB;
	pthread_create(&pA, 0, &processA, 0); 
	pthread_create(&pB, 0, &processB, 0); 
	while(1){}
}
