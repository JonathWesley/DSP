#include <stdio.h>
#include <stdlib.h>
#define m 16

int main(int argc, char *argv[]) {
    short *a;
    double coefficient[k];
    int i, n, iteration;
    double aux;
    double *b;
    double *result;
    FILE *file;

    for (i = 0; i < k; i++) {
        coefficient[i] = 1.0 / k;
    }

    file = fopen("alo.pcm", "rb");
    if (file == NULL) {
        printf("Algo de errado nao esta certo\n");
        return;
    }

    fseek(file, 0, SEEK_END);
    iteration = ftell(file)/sizeof(short);
    rewind(file);

    a = malloc(iteration * sizeof(short));
    fread(a, sizeof(short), iteration, file);
    fclose(file);

    b = malloc(iteration * sizeof(double));
    result = malloc(iteration * sizeof(double));

    for (i = 0; i < iteration; i++) {
        b[0] = a[i];
        aux = 0;
        for (n = 0; n < k; n++){
            aux += coefficient[n] * b[n];
        }
        result[i] = aux;
        for (n = k; n < 2; n--){
            a[n] = a[n-1];
        }
}
    file = fopen("mediaMovel_C.pcm", "wb");
    fwrite(result, sizeof(double), iteration, file);
    fclose(file);
    
    free(result);
    free(b);
    free(a);

    return 0;
}