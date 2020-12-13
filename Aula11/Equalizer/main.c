#include <stdio.h>
#include <fcntl.h>
#include <io.h>

#define NUMERO_SAMPLES 160

int main() {
  FILE * in_file, * out_file;
  int i, n, n_amost;

  short entrada, saida;
  short sample[NUMERO_SAMPLES] = {
    0x0
  };

  float yPB, yPA, yPF, y, gPB = 0.7, gPF = 0.5, gPA = 0.3;

  float coefPB[NUMERO_SAMPLES] = {
    #include "coeficientesPB.dat"
  };

  float coefPA[NUMERO_SAMPLES] = {
    #include "coeficientesPA.dat"
  };

  float coefPF[NUMERO_SAMPLES] = {
    #include "coeficientesPF.dat"
  };

  /* abre os arquivos de entrada e saida */
  if ((in_file = fopen("Sweep_3800.pcm", "rb")) == NULL) {
    printf("\nErro: Nao abriu o arquivo de entrada\n");
    return 0;
  }
  if ((out_file = fopen("saida_equalizador.pcm", "wb")) == NULL) {
    printf("\nErro: Nao abriu o arquivo de saida\n");
    return 0;
  }

  // zera vetor de amostras
  for (i = 0; i < NUMERO_SAMPLES; i++) {
    sample[i] = 0;
  }

  // execução do filtro
  do {

    //zera saída do filtro
    y = 0;
    yPA = 0;
    yPB = 0;
    yPF = 0;

    //lê dado do arquivo
    n_amost = fread( & entrada, sizeof(short), 1, in_file);
    sample[0] = entrada;

    //Convolução e acumulação
    for (n = 0; n < NUMERO_SAMPLES; n++) {
      yPB += coefPB[n] * sample[n];
    }

    for (n = 0; n < NUMERO_SAMPLES; n++) {
      yPA += coefPA[n] * sample[n];
    }

    for (n = 0; n < NUMERO_SAMPLES; n++) {
      yPF += coefPF[n] * sample[n];
    }


    //desloca amostra
    for (n = NUMERO_SAMPLES - 1; n > 0; n--) {
      sample[n] = sample[n - 1];
    }

    y = (yPA*gPA) + (yPB*gPB) + (yPF*gPF);

    saida = (short) y;

    //escreve no arquivo de saída
    fwrite( & saida, sizeof(short), 1, out_file);

  } while (n_amost);

  //fecha os arquivos de entrada de saída
  fclose(out_file);
  fclose(in_file);
  return 0;
}
