#include <stdio.h>
#include <math.h>
#include <fract.h>
#include <cycles.h>
#include <string.h>

#define PI 3.14159265359

float ff[2] = {0,0}, fb[2] = {0,0};

void biquadWah(fract16 *in, fract16 Fs, float lfo, char Q, char wet, fract16 *out) {
    // Convert value of LFO to normalized frequency

    float w0 = 2*PI*lfo/Fs;
    // Normalize bandwidth
    float alpha = sin(w0)/(2*Q);
    float b0 = (1-cos(w0))/2;
    float a0 = 1+alpha;
    float b1 = 1-cos(w0);
    float a1 = -2*cos(w0);
    float b2 = (1-cos(w0))/2;
    float a2 = 1-alpha;
    // Wet/dry mix
    char mixPercent = wet; // 0 = only dry, 100 = only wet
    float mix = (float)mixPercent/100;
    // Store dry and wet signals
    float drySig = (float)*in;
    // Low-pass filter
    float wetSig = (b0/a0)*(*in);
    wetSig += (b1/a0)*ff[0] + (b2/a0)*ff[1] - (a1/a0)*fb[0] - (a2/a0)*fb[1];
    // Blend parallel paths
    *out = ((1-mix)*drySig + mix*wetSig);
    // Iterate buffers for next sample
    ff[1] = ff[0];
    ff[0] = (float)*in;
    fb[1] = fb[0];
    fb[0] = wetSig;
}

int main( void ) {
	
	cycle_stats_t stats;
	
	fract16 Fs = 8000;
    float Ts = 1 / (float)Fs;
    float rate = 0.5;
    fract16 centerFreq = 1500;
    fract16 depth = 1000;
    
    char Q = 7, wet = 100;
    fract16 entrada = 0;
    int tam = 0;
    	
    CYCLES_INIT(stats);
    
	//arquivo de entrada e saída
    FILE *f_in, *f_out;
    f_in = fopen("..\\input.pcm", "rb");
    f_out = fopen("..\\output.pcm", "wb");
    if(!f_in || !f_out){
        printf("Erro no carregamento de arquivo");
        return 1;
    }
    
    fract16 buffer;
    // tam arquivo
    while(fread(&buffer, sizeof(short), 1, f_in)){
        tam++;
    }
    
	rewind (f_in); /// VOLTA O CURSOR NO INICIO
    
    int i = 0;
    fract16 out;
    
    float t = 0;
    float lfo = 0;

    printf("Processando ...\n ");
    
    for(i = 1; i< tam; i++){
    	fread(&buffer,sizeof(short),1,f_in);
    	
    	CYCLES_START(stats);
    	
        t = (i-1) * Ts;
        lfo = sin(2*PI*rate*t);
        lfo *= depth;
        lfo += centerFreq;
        biquadWah(&buffer, Fs, lfo, Q, wet, &out);
        
        CYCLES_STOP(stats);
        
        fwrite(&out, sizeof(short), 1, f_out); // Funciona
    }
    
    printf("terminado!\n");
		
    CYCLES_PRINT(stats);
    
    /**/
    fclose(f_in);
    fclose(f_out);
	
	return 0;
}
