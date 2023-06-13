#include<stdio.h>

int main(){
	int i;
	for(i=0; i<10; i++)printf("hello, world\n");
	printf("%d\n",i);{
		int t = 1;
		printf("%d\n", t);
	}
	int t = 5;
	printf("%d\n", t);
	return 0;
}