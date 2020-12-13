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

    if((Data_out = fopen("Overdrive_CFLOAT.pcm", "wb")) == NULL){

        printf("\nErro: Nao abriu o arquivo de saida");
        return 0;
    }

    short Num_Amostra, Amostra;
    float Amostra_norm, Threshold = 0.333333;
    int count = 1;

    do{

        Num_Amostra = fread(&Amostra, sizeof(short), 1, Data_in);
        Amostra_norm = (float)Amostra;

        if (Amostra_norm != 0)
            Amostra_norm = Amostra_norm / MaxValue;

        if(Amostra_norm <= Threshold && Amostra_norm > 0)
            Amostra_norm = Amostra_norm * 2;

        else if(Amostra_norm >= (-1 * Threshold) && Amostra_norm < 0)
            Amostra_norm = Amostra_norm * 2;

        if(Amostra_norm >= Threshold)
            Amostra_norm = (3 - ((2 - (3 * Amostra_norm)) * (2 - (3 * Amostra_norm)))) / 3;

        if (Amostra_norm <= (-1 * Threshold))
            Amostra_norm = (-1 * (3 - ((2 - (3 * Amostra_norm * -1)) * (2 - (3 * Amostra_norm * -1))))) / 3;

        if(Amostra_norm >= 0.666666)
            Amostra_norm = 1;

        if(Amostra_norm <= -0.666666)
            Amostra_norm = -1;

        Amostra = (short)(Amostra_norm * MaxValue);
        fwrite(&Amostra, sizeof(short), 1, Data_out);

    }while(Num_Amostra);

    fclose(Data_in);
    fclose(Data_out);

    return 0;
}
