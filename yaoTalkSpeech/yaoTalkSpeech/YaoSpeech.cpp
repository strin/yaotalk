#include "Python.h"
#include <pocketsphinx.h>
#include "portaudio.h"
#include "stdio.h"
#include "time.h"
#include <fcntl.h>
#include <string>
#include "sys/stat.h"

#define MODELDIR "/usr/local/share/pocketsphinx/model"
#define SAMPLE_RATE (16000)

using namespace std;

ps_decoder_t *ps;
cmd_ln_t *config;
FILE *buffer = NULL;
PaStream *stream;
char const *hyp, *uttid;
int rv;
int32 score;

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
}

static PyObject* listen(PyObject *self, PyObject *args)
{
	if(buffer != NULL) return Py_BuildValue("");
	buffer = fopen("buffer.raw", "w+");
	fprintf(stdout, "microphone: started.\n");
	PaError  err = Pa_OpenDefaultStream( &stream,
							   1,          /* input channel */
							   0,          /* no output */
							   paInt16,
							   SAMPLE_RATE,
							   1024,         /* frames per buffer, i.e. the number
											of sample frames that PortAudio will
											request from the callback. Many apps
											may want to use
											paFramesPerBufferUnspecified, which
											tells PortAudio to pick the best,
											possibly changing, buffer size.*/
							   patestCallback, /* this is your callback function */
							   buffer); /*This is a pointer that will be passed to
										 your callback*/
	err = Pa_StartStream(stream);
	return Py_BuildValue("i", err);
}

static PyObject* speak(PyObject *self, PyObject *args) {
	const char* message;
	if (!PyArg_ParseTuple(args, "s", &message)) 
		return Py_BuildValue("");
	int res = system(("/usr/bin/say -v Ting-Ting "+string(message)).c_str());
	return Py_BuildValue("i", res);
}

static PyObject* recognize(PyObject *self, PyObject *args) {
	Pa_StopStream(stream);
	fprintf(stdout, "microphone: ended.\n");
	fseek(buffer, 0, SEEK_SET);
	rv = ps_decode_raw(ps, buffer, "buffer", -1);
	buffer = NULL;
	if (rv < 0)
		return Py_BuildValue("");
	hyp = ps_get_hyp(ps, &score, &uttid);
	if (hyp == NULL)
		return Py_BuildValue("");
	return Py_BuildValue("s", hyp);
}


static PyMethodDef YaoSpeechMethods[] = {
    {"listen",  listen, METH_VARARGS,
     "start listening until recognize a segnment of speech."},
     {"recognize", recognize, METH_VARARGS,
     "recognize the speech currently it listens to."
 	},
 	{"speak", speak, METH_VARARGS,
     "speak a sentense using TTS."
 	},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initYaoSpeech(void)
{
    (void) Py_InitModule("YaoSpeech", YaoSpeechMethods);

 //    printf("1\n");
	// int fplog = open("log.txt", O_CREAT | O_RDWR | S_IREAD | S_IWRITE);
	// printf("2\n");
	// dup2(1, fplog);
	// printf("3\n");
    // freopen("log.txt", "a+", stdout);

	config = cmd_ln_init(NULL, ps_args(), TRUE,
					 "-hmm", MODELDIR "/hmm/zh_broadcastnews_ptm256_8000",
					 "-lm",  "resource/speech.lm",
					 "-dict",  "resource/speech.dic",
					 NULL);

    //	config = cmd_ln_init(NULL, ps_args(), TRUE,
//						 "-hmm", MODELDIR "/hmm/en_US/hub4wsj_sc_8k",
//						 "-lm", MODELDIR "/lm/en/turtle.DMP",
//						 "-dict", MODELDIR "/lm/en/turtle.dic",
//						 NULL); // sample rate 16000.

    if (config == NULL) {
    	fprintf(stderr, "configuration: failed.\n");
		return;
    }
	ps = ps_init(config);
	if (ps == NULL) {
		fprintf(stderr, "decoder: cannot init config.\n");
		return;
	}
	PaError err = Pa_Initialize();
	if(err != paNoError) printf(  "PortAudio error: %s\n", Pa_GetErrorText( err ) );

	return;
}



