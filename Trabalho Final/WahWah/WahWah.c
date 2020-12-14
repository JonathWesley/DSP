#include <stdio.h>
#include <math.h>
#include <fract.h>
#include <cycles.h>
#include <string.h>

#define PI 3.14159265359

float ff[2] = {0,0}, fb[2] = {0,0};

void biquadWah(fract16 *in, fract16 Fs, float lfo, char Q, char wet, fract16 *out) {
    // converte o valor do LFO para normalizar a frequencia

    float w0 = 2*PI*lfo/Fs;
    // normaliza a largura de banda
    float alpha = sin(w0)/(2*Q);
    float b0 = (1-cos(w0))/2;
    float b1 = 1-cos(w0);
    float b2 = (1-cos(w0))/2;
    float a0 = 1+alpha;
    float a1 = -2*cos(w0);
    float a2 = 1-alpha;
    // Wet/dry mix
    char mixPercent = wet; // 0 = dry, 100 = wet
    float mix = (float)mixPercent/100;
    // guarda o sinal dry
    float drySig = (float)*in;
    // filtro passa baixa
    float wetSig = (b0/a0)*(*in);
    wetSig += (b1/a0)*ff[0] + (b2/a0)*ff[1] - (a1/a0)*fb[0] - (a2/a0)*fb[1];
    // junta os sinais do dry e wet
    *out = ((1-mix)*drySig + mix*wetSig);
    // itera o buffer para proxima amostra
    ff[1] = ff[0];
    ff[0] = (float)*in;
    fb[1] = fb[0];
    fb[0] = wetSig;
}

int main( void ) {
	
	// declara a estrutura para contar os ciclos
	cycle_stats_t stats;
	
	// frequencia de amostragem
	fract16 Fs = 8000;
	// periodo de amostragem
    float Ts = 1 / (float)Fs;
    float rate = 0.5;
    fract16 centerFreq = 1500;
    fract16 depth = 1000;
    
    // deve ser entre 1 e 500
    char Q = 7;
    // deve ser entre 0 e 100
    char wet = 100;
    
    fract16 entrada = 0;
    	 
    // inicializa a estrutura
    CYCLES_INIT(stats);
    
	// arquivo de entrada e saída
    FILE *f_in, *f_out;
    f_in = fopen("..\\jazz.pcm", "rb");
    f_out = fopen("..\\output.pcm", "wb");
    if(!f_in || !f_out){
        printf("Erro no carregamento de arquivo");
        return 1;
    }
    
    // entrada
    fract16 buffer;
    // tam arquivo
    int tam = 0;
    while(fread(&buffer, sizeof(short), 1, f_in)){
        tam++;
    }
    
    // volta o cursor para o inicio do arquivo
	rewind (f_in);
    
    int i = 0;
    // saida
    fract16 out;
    
    float t = 0;
    // low-frequency oscillator
    float lfo = 0;

    printf("Processando ...\n ");
    
    for(i = 1; i< tam; i++){
    	fread(&buffer,sizeof(short),1,f_in);
    	
    	// comeca a contagem de ciclos
    	CYCLES_START(stats);
    	
        t = (i-1) * Ts;
        lfo = sin(2*PI*rate*t);
        lfo *= depth;
        lfo += centerFreq;
        biquadWah(&buffer, Fs, lfo, Q, wet, &out);
        
        // para a contagem de ciclos
        CYCLES_STOP(stats);
        
        fwrite(&out, sizeof(short), 1, f_out);
    }
    
    printf("terminado!\n");
		
    // imprime o resultado da contagem de ciclos
    CYCLES_PRINT(stats);
    
    // fecha os arquivos
    fclose(f_in);
    fclose(f_out);
	
	return 0;
}
