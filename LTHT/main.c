void fib (int n);
int main (int argc, char** argv) {

	int n = 0;
	sscanf(argv[1], "%d", &n);
	fib(n);

}
