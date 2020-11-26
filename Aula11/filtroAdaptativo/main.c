#include <stdio.h>
#include <fcntl.h>
#include <io.h>

#define NSAMPLES 160
#define MU 0.000000000005

int main() {
  FILE *in_file, *out_file, *out_file_error;
  int i, n, n_amost;

  short entrada, saida, saida_erro, xn[NSAMPLES];

  double wn [NSAMPLES];
  double dn = 0.0;
  double yn = 0.0;
  double erro = 0.0;

  //Carregando os coeficientes
  float coef[NSAMPLES] = {
        #include "coeficientesPA.dat" // NSAMPLES
  };

  /* abre os arquivos de entrada e saida */
  if ((in_file = fopen("wn.pcm", "rb")) == NULL) {
    printf("\nErro: Nao abriu o arquivo de entrada\n");
    return 0;
  }
  if ((out_file = fopen("saida_filtro_adaptativo.pcm", "wb")) == NULL) {
    printf("\nErro: Nao abriu o arquivo de saida\n");
    return 0;
  }
  if ((out_file_error = fopen("erro_filtro_adaptativo.pcm", "wb")) == NULL) {
    printf("\nErro: Nao abriu o arquivo de saida\n");
    return 0;
  }


  // zera vetor de amostras
  for (i = 0; i < NSAMPLES; i++) {
    // entrada
    xn[i] = 0;
    // coneficientes gerados
    wn[i] = 0.0;
  }

  do {

    // saida desejada
    dn = 0;
    // saida gerada
    yn = 0;

    // lê wn do arquivo
    n_amost = fread( & entrada, sizeof(short), 1, in_file);
    xn[0] = entrada;


    // convolução da saída do filtro y(n)
    for (n = 0; n < NSAMPLES; n++) {
      // gera saida a partir dos coeficientes gerados pelo filtro
      yn += wn[n] * xn[n];
    }

    // convolução do sinal desejado d(n)
    for (n = 0; n < NSAMPLES; n++) {
      // gera a saida do sistema "desconhecido"
      dn += coef[n] * xn[n];
    }

    // erro = saida desejada - saida gerada
    erro = dn - yn;
    //printf("Erro: %f\n", erro);

    // atualizando os coeficientes do filtro usando lms
    for (n = 0; n < NSAMPLES; n++) {
        // novos coeficientes = coeficientes antigos + taxa de aprendizagem * erro * entrada
        wn[n] = wn[n] + MU * erro * xn[n];
    }

    // atualizando o x(n)
    for (n = NSAMPLES - 1; n > 0; n--) {
      // desloca entrada pra pegar proximo primeiro valor
      xn[n] = xn[n - 1];
    }

    saida = (short) yn;
    saida_erro = (short) erro;

    //escreve no arquivo de saída
    fwrite( & saida, sizeof(short), 1, out_file);
    fwrite( & saida_erro, sizeof(short), 1, out_file_error);

  } while (n_amost);

  //fecha os arquivos de entrada de saída
  fclose(out_file);
  fclose(in_file);
  return 0;
}
