#include<pthread.h>
#include<stdio.h>
#include<semaphore.h>
#include<time.h>

int a[9999];
sem_t sem;
static int count = 0;
int n;
int i;

void *processA(){
	while(1){
		if(count<n){
			srand((int) time(0));
			a[i++] = rand() %(n-1);
			count++;
			printf("So phan tu cua mang la: %d\n", count);
		}
		int time_sleep = rand() % 2 + 2;
		sleep(1);
		sem_post(&sem);
	}
}

void* processB()
{
	while (1)
	{
		sem_wait(&sem);			
			if (count == 0)
			{
				printf("Khong co phan tu nao trong mang!!");
			}
			else
			{
				count--;
				for (int j = 0; j < count; j++)
				{
					a[j] = a[j + 1];
				}
				
				printf("\nSo phan tu cua mang sau khi pop la: %d\n", count);
			}
		int time_sleep = rand() % 2 + 1;
		sleep(4);	
	}
}


int main(){
	sem_init(&sem,0,0);
	printf("Nhap so phan tu cua mang: ");
	scanf("%d", &n);
	pthread_t pA, pB;
	pthread_create(&pA, 0, &processA, 0); 
	pthread_create(&pB, 0, &processB, 0); 
	while(1){}
}
