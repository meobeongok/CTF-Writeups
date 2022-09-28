#include<stdio.h>
#include<pthread.h>
#include<signal.h>
#include<unistd.h>

int loop_forever = 1;

void on_sigint(){
	system("killall vim");
	printf("\nCRT+C is pressed!\n");
	loop_forever = 0;
}

void *open_vim(){
	system("vim abcd.txt");
}

int main(){
	loop_forever = 1;
	pthread_t tid;
	printf("Welcome to IT007, I am 20521859\n");
	pthread_create(&tid,NULL, &open_vim, NULL);
	signal(SIGINT, on_sigint);
	while(loop_forever){}
	return 0;
}
