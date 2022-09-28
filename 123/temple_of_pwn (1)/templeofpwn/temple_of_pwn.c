#include<stdio.h>
#include <string.h>
#include <stdlib.h>

char s[32];
long* right_whisper;

void first_step(char *whisper, size_t length) {
    puts("You need to whisper something to make the monster sleep");
    puts("Length of your whisper: ");
    scanf("%lu", &length);
    whisper = (char*)malloc(length);
    whisper[length - 1] = 0;
    if (*right_whisper == 0)
        next_step(right_whisper);
}

void next_step(long *a) {
    printf("Looks like you've passed the first test, it's time for the second one\n");
    char buf[32];
    puts("You have overcome the monster, now pray to the god of pwn to give you the reward");
    puts("You good. It's time to get the reward!");
    read(0,buf,100); 
    return puts("Bye");
}

int main() {
    char* whisper;
    size_t length;
    size_t choice;
    puts("Welcome to Temple of pwn");
    puts("Enter your name: ");
    read(0, s, 32);
    right_whisper = malloc(0x50000);
    printf("Hello %s", s);   
    puts("Now you have 2 choices");
    puts("1. Enter the temple, against the monsters and get the reward ");
    puts("2. Run");
    puts("Enter your choice:");
    scanf("%lu", &choice);
    *right_whisper = choice;
    switch (choice) {
    case 1:       
        puts("Okay, Let's go to the temple");
        first_step(whisper,length);
        break;
    case 2:
        puts("Bye!");
        exit(1);
    default:
        puts("Wrong choice!");
        exit(1);
    }
    return 0;
}
