from distutils.core import setup, Extension
import os

module = Extension('YaoSpeech',
                    include_dirs = ['/usr/local/include', '/usr/local/include/sphinxbase', '/usr/local/include/pocketsphinx'],
                    libraries = ['portaudio', 'pocketsphinx', 'sphinxbase', ],
                    library_dirs = ['/usr/local/lib/', '/usr/local/Cellar/portaudio/19.20111121/lib'],
                    sources = ['YaoSpeech.cpp'])

setup (name = 'YaoSpeech',
       version = '1.0',
       description = 'Speech Recognition and Sythesis for YaoTalk Project.',
       author = 'Tianlin Shi',
       author_email = 'stl501@gmail.com',
       url = '',
       long_description = '',
       ext_modules = [module])

os.system('cp build/lib.macosx-10.8-x86_64-2.7/YaoSpeech.so ./')