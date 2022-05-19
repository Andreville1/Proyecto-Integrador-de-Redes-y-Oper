// followed this tutorial : https://www.youtube.com/watch?v=ZS3qxIjZ0z0

#include <stdlib.h>
#include <stdio.h>
#include <string.h> 
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>

#define string_len 200

int main(int argc, char* argv[]) {
    int fd[2];

    if( pipe(fd) == -1){
        return 1;
    }

    int pid = fork();
 
    if (pid < 0){
        return 2; 
    }

    if (pid == 0) {
        // child process
        close(fd[0]);
        char str[string_len];
        printf(" Input operation: ");
        fgets(str, string_len, stdin);
        str[strlen(str)-1] = '\0';

        int n = strlen(str) + 1;
        if ( write(fd[1], &n, sizeof(int)) < 0){
            return 4;
        }

        if ( write(fd[1], str, sizeof(char) * n) < 0 ){
            return 3;
        }
        close(fd[1]);

    } else { 

        // Parent process
        close(fd[1]);
        char str[string_len];
        int n;

        if ( read(fd[0], &n, sizeof(int)) < 0) {
            return 5;
        }
        if ( read(fd[0], str, sizeof(char) * n) < 0) {
            return 6;
        }

        printf(" Received: %s\n", str);
    }
    return 0; 
}