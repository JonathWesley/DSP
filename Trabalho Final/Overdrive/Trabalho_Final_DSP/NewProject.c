#include <stdio.h>
#include <stdlib.h>

#define len 9600
#define MaxValue 31809

int main(){

    FILE *Data_in, *Data_out;

    if((Data_in = fopen("Guitar_test.pcm", "rb")) == NULL){

        printf("\nErro: Nao abriu o arquivo de entrada");
        return 0;
    }

    if((Data_out = fopen("Overdrive_CSHORT.pcm", "wb")) == NULL){

        printf("\nErro: Nao abriu o arquivo de saida");
        return 0;
    }

    fract16 Num_Amostra, Amostra, Threshold = MaxValue * 1/3;
    float Aux;

    do{

        Num_Amostra = fread(&Amostra, sizeof(short), 1, Data_in);

        if(Amostra <= Threshold && Amostra > 0)
            Amostra = Amostra * 2;

        else if(Amostra >= (-1 * Threshold) && Amostra < 0)
            Amostra = Amostra * 2;

        if(Amostra >= Threshold){

            Aux = (float)Amostra / MaxValue;
            Amostra = (fract16)(((3 - ((2 - (3 * Aux)) * (2 - (3 * Aux)))) / 3) * MaxValue);
        }

        if(Amostra <= (Threshold * -1)){

            Aux = (float)Amostra / MaxValue;
            Amostra = (fract16)(((-1 * (3 - ((2 - (3 * Aux * -1)) * (2 - (3 * Aux * -1))))) / 3) * MaxValue);
        }

        if(Amostra >= (2 * Threshold))
            Amostra = MaxValue;

        if(Amostra <= (-2 * Threshold))
            Amostra = (-1 * MaxValue);

        fwrite(&Amostra, sizeof(short), 1, Data_out);

    }while(Num_Amostra);

    fclose(Data_in);
    fclose(Data_out);

    return 0;
}
