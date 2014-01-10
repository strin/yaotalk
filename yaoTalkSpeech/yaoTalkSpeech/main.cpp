#include <pocketsphinx.h>
#include "portaudio.h"
#include "stdio.h"
#include "time.h"


#define MODELDIR "/usr/local/share/pocketsphinx/model"
#define SAMPLE_RATE (16000)


typedef struct
{
    float left_phase;
    float right_phase;
}   
paTestData;

ps_decoder_t *ps;
cmd_ln_t *config;
FILE *fh;
char const *hyp, *uttid;
int16 buf[20480];
int rv;
int32 score;

template <typename T>
T swap_endian(T u)
{
    union
    {
        T u;
        unsigned char u8[sizeof(T)];
    } source, dest;
	
    source.u = u;
	
    for (size_t k = 0; k < sizeof(T); k++)
        dest.u8[k] = source.u8[sizeof(T) - k - 1];
	
    return dest.u;
}

/* This routine will be called by the PortAudio engine when audio is needed.
   It may called at interrupt level on some machines so don't do anything
   that could mess up the system like calling malloc() or free().
*/ 
static int patestCallback( const void *inputBuffer, void *outputBuffer,
                           unsigned long framesPerBuffer,
                           const PaStreamCallbackTimeInfo* timeInfo,
                           PaStreamCallbackFlags statusFlags,
                           void *userData )
{
    /* Cast data passed through stream to our structure. */
	if(inputBuffer != NULL) {
		int16* data = (int16*)inputBuffer;
		FILE* fpout = (FILE*)userData;
		fwrite(data, 2, framesPerBuffer, fpout);
		fflush(fpout);
	}
	return 0;
	if(userData == NULL) return 0;
    paTestData *data = (paTestData*)userData; 
    float *out = (float*)outputBuffer;
    unsigned int i;
    (void) inputBuffer; /* Prevent unused variable warning. */
    
    for( i=0; i<framesPerBuffer; i++ )
    {
        *out++ = data->left_phase;  /* left */
        *out++ = data->right_phase;  /* right */
        /* Generate simple sawtooth phaser that ranges between -1.0 and 1.0. */
        data->left_phase += 0.01f;
        /* When signal reaches top, drop back down. */
        if( data->left_phase >= 1.0f ) data->left_phase -= 2.0f;
        /* higher pitch so we can distinguish left and right. */
        data->right_phase += 0.03f;
        if( data->right_phase >= 1.0f ) data->right_phase -= 2.0f;
    }
    return 0;
}

int test() {
	ps_decoder_t *ps;
	cmd_ln_t *config;
	FILE *fh;
	char const *hyp, *uttid;
	int16 buf[512];
	int rv;
	int32 score;
	
	config = cmd_ln_init(NULL, ps_args(), TRUE,
						 "-hmm", MODELDIR "/hmm/zh/tdt_sc_8k",
						 "-lm", MODELDIR "/lm/zh_CN/gigatdt.5000.DMP",
						 "-dict", MODELDIR "/lm/zh_CN/mandarin_notone.dic",
						 NULL);
	if (config == NULL)
		return 1;
	ps = ps_init(config);
	if (ps == NULL)
		return 1;
	
	fh = fopen("test.raw", "rb");
	if (fh == NULL) {
		perror("Failed to open goforward.raw");
		return 1;
	}
	
	rv = ps_decode_raw(ps, fh, "goforward", -1);
	if (rv < 0)
		return 1;
	hyp = ps_get_hyp(ps, &score, &uttid);
	if (hyp == NULL)
		return 1;
	printf("Recognized: %s\n", hyp);
	
	fseek(fh, 0, SEEK_SET);
	rv = ps_start_utt(ps, "goforward");
	if (rv < 0)
		return 1;
	while (!feof(fh)) {
		size_t nsamp;
		nsamp = fread(buf, 2, 512, fh);
		rv = ps_process_raw(ps, buf, nsamp, FALSE, FALSE);
	}
	rv = ps_end_utt(ps);
	if (rv < 0)
		return 1;
	hyp = ps_get_hyp(ps, &score, &uttid);
	if (hyp == NULL)
		return 1;
	printf("Recognized: %s\n", hyp);
	
	fclose(fh);
	ps_free(ps);
	return 0;
}

int main(int argc, char *argv[])
{
	config = cmd_ln_init(NULL, ps_args(), TRUE,
						 "-hmm", MODELDIR "/hmm/zh_broadcastnews_ptm256_8000",
						 "-lm", "3850.lm",
						 "-dict", "speech.dic",
						 NULL);
//	config = cmd_ln_init(NULL, ps_args(), TRUE,
//						 "-hmm", MODELDIR "/hmm/en_US/hub4wsj_sc_8k",
//						 "-lm", MODELDIR "/lm/en/turtle.DMP",
//						 "-dict", MODELDIR "/lm/en/turtle.dic",
//						 NULL); // sample rate 16000.
	if (config == NULL)
		return 1;
	ps = ps_init(config);
	if (ps == NULL)
		return 1;
	
	// fh = fopen("haha.wav", "rb");
	// if (fh == NULL) {
	// 	perror("Failed to open goforward.raw");
	// 	return 1;
	// }
	
	// rv = ps_decode_raw(ps, fh, NULL, -1);
	// if (rv < 0)
	// 	return 1;
	// hyp = ps_get_hyp(ps, &score, &uttid);
	// if (hyp == NULL)
	// 	return 1;
	// printf("Recognized: %s\n", hyp);
	
	PaError err = Pa_Initialize();
	if(err != paNoError) printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );
	PaStream *stream;
	FILE* fpout = fopen("test.raw", "w+");
    /* Open an audio I/O stream. */
    err = Pa_OpenDefaultStream( &stream,
							   1,          /* input channel */
							   0,          /* no output */
							   paInt16,
							   SAMPLE_RATE,
							   128,         /* frames per buffer, i.e. the number
											of sample frames that PortAudio will
											request from the callback. Many apps
											may want to use
											paFramesPerBufferUnspecified, which
											tells PortAudio to pick the best,
											possibly changing, buffer size.*/
							   patestCallback, /* this is your callback function */
							   fpout ); /*This is a pointer that will be passed to
										 your callback*/
	fprintf(stdout, "microphone: started.\n");
	err = Pa_StartStream(stream);
    if (rv < 0)
            return 1;
	
	time_t ta, tb;
	time(&ta);
	while(true) {
		time(&tb);
		if((tb-ta) > 2) break;
		system("sleep 0.2");
	}
	Pa_StopStream(stream);
	fprintf(stdout, "microphone: ended.\n");
	fseek(fpout, 0, SEEK_SET);
	rv = ps_decode_raw(ps, fpout, "goforward", -1);
	if (rv < 0)
		return 1;
	hyp = ps_get_hyp(ps, &score, &uttid);
	if (hyp == NULL)
		return 1;
	printf("Recognized: %s\n", hyp);

	
//	rv = ps_start_utt(ps, "goforward");
//	if (rv < 0)
//		return 1;
//	while (!feof(fpout)) {
//		size_t nsamp;
//		nsamp = fread(buf, 2, 2048, fpout);
//		rv = ps_process_raw(ps, buf, nsamp, FALSE, FALSE);
//	}
//	rv = ps_end_utt(ps);
//	if (rv < 0)
//		return 1;
//	hyp = ps_get_hyp(ps, &score, &uttid);
//	if (hyp == NULL)
//		return 1;
//	printf("Recognized: %s\n", hyp);
//	fclose(fpout);
	return 0;
}



