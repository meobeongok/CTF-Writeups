#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void sig_handler(int signum)
{
	puts("Time out!");
	exit(0);
}

void init_alarm()
{
	signal(SIGALRM, sig_handler);
	alarm(120);
}

void init()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

void Buy(long long int *p)
{
	unsigned int idnumber, size;

	printf("Orange number: ");
	scanf("%u", &idnumber);
	printf("Size: ");
	scanf("%u", &size);
	if ((idnumber > 1) || (size > 0x1000))    // Avoid house of force
	{
		printf("Not allowed!");
		exit(0);
	}

	p[idnumber] = (long long int)malloc(size);
}

void Modify(long long int *p)
{
	unsigned char *orange;
	unsigned int cell, idnumber;

	printf("Orange number: ");
	scanf("%u", &idnumber);
	if ((idnumber > 1) || (p[idnumber]==0))
	{
		printf("Not allowed!");
		exit(0);
	}
	orange = (unsigned char*)p[idnumber];

	printf("Total %u cell in this orange\n", *(unsigned int*)(p[idnumber]-8) & 0xfffffff0);
	printf("Cell index: ");
	scanf("%u", &cell);

	printf("Current value: %hhu\n", *(orange + cell));
	printf("New value: ");
	scanf("%hhu", &orange[cell]);
}

int main()
{
	int d;
	long long int p[2];

	init();
	init_alarm();
	p[0] = 0;
	p[1] = 0;
	while (1)
	{
		puts("1. Buy an orange");
		puts("2. Modify part of orange");
		puts("3. Exit");
		printf("> ");
		scanf("%d", &d);
		if (d==2)
			Modify(p);
		else if (d==1)
			Buy(p);
		else
			break;
	}

	return 0;
}