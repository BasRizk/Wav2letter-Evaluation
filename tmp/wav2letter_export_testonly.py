#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
# Copyright 2019 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# export speech training data to create a wav2letter case
#

import sys
import logging
import os
import codecs

from optparse               import OptionParser

from nltools                import misc
from nltools.tokenizer      import tokenize
from nltools.phonetics      import ipa2xsampa

from speech_lexicon         import Lexicon
from speech_transcripts     import Transcripts

APP_NAME = 'W2L TEST SET FORMATTER'

#ASR_MODELS_DIR      = 'data/dst/asr-models'


#
# main
#

misc.init_app(APP_NAME)

#
# commandline
#

parser = OptionParser("usage: %prog [options] <dictionary> <language> <audio_corpus> [ <audio_corpus2> ... ]")

parser.add_option ("-d", "--debug", dest="debug", type='int', default=0, help="Limit number of sentences (debug purposes only), default: 0")

parser.add_option ("-l", "--lang", dest="lang", type = "str", default='de', help="language (default: de)")

parser.add_option ("-p", "--prompt-words", action="store_true", dest="prompt_words", help="Limit dict to tokens covered in prompts")

parser.add_option ("-v", "--verbose", action="store_true", dest="verbose", help="verbose output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) < 2:
    parser.print_usage()
    sys.exit(1)

dictionary     = args[0]
audio_corpora  = args[1:]

LANG = options.lang
dictionary = LANG + "/" + dictionary
LANGUAGE_MODELS_DIR = 'models/' + LANG
language_model_dir = LANGUAGE_MODELS_DIR

if not os.path.isdir(language_model_dir):
    logging.error(
        "Could not find language model directory {}. Create a language "\
        .format(language_model_dir))
    sys.exit(1)

work_dir = 'tests'
data_dir = work_dir + "/" + LANG + "-data" 

#
# load dict
#

logging.info("loading lexicon...")
lex = Lexicon(file_name=dictionary)
logging.info("loading lexicon...done.")

#
# export audio
#

cnt = 0

def export_audio (train_val, tsdict):

    global data_dir, utt_num, options, cnt

    destdirfn = data_dir

    lcnt = 0


    for utt_id in tsdict:

        ts = tsdict[utt_id]

        tokens = tokenize(ts['ts'], lang=options.lang)
        covered_by_lex = True
        for token in tokens:
            if not (token in lex):
                logging.error(u'token %s missing from dict!' % token)
                logging.error(u'utt_id: %s' % utt_id)
                logging.error(u'ts: %s' % ts['ts'])
                covered_by_lex = False
                break

        if not covered_by_lex:
            continue
        
        print("about to export")
        with codecs.open('%s/%09d.id'  % (destdirfn, utt_num[train_val]), 'w', 'utf8') as idf,   \
             codecs.open('%s/%09d.tkn' % (destdirfn, utt_num[train_val]), 'w', 'utf8') as tknf,  \
             codecs.open('%s/%09d.wrd' % (destdirfn, utt_num[train_val]), 'w', 'utf8') as wrdf   :
            print("utterance read. " + str(wrdf) + "\n")
            tkn = u''
            wrd = u''
            for token in tokens:

                ipas = lex[token]['ipa'] 
                xsr = ipa2xsampa(token, ipas, spaces=True)

                xs = (xsr.replace('-', '')
                         .replace('\' ', '\'')
                         .replace('  ', ' ')
                         .replace('#', 'nC'))

                if tkn:
                    tkn += u' | '
                    wrd += u' '

                tkn += xs
                wrd += token
                
            tknf.write('%s\n' % tkn)
            wrdf.write('%s\n' % wrd)
            idf.write('utt_id\t%s\ncorpus\t%s\nlang\t%s\n' % (utt_id, ts['corpus_name'], options.lang))
            
            os.symlink('%s/%s/%s.wav' % (work_dir, ts['corpus_name'], utt_id), '%s/%09d.wav' % (destdirfn, utt_num[train_val]))
            # cmd = 'ln -s %s/%s/%s.wav %s/%09d.wav' % (wav16_dir, ts['corpus_name'], utt_id, destdirfn, utt_num[train_val])
            # logging.debug(cmd)
            # os.system(cmd)

            # utt2spkf.write('%s %s\n' % (utt_id, ts['spk']))

            utt_num[train_val] = utt_num[train_val] + 1

        cnt  += 1
        lcnt += 1
        if cnt % 1000 == 0:
            logging.info ('%6d audio files linked from %s [%s] (%6d/%6d)...' % (cnt, ts['corpus_name'], train_val, lcnt, len(tsdict)))

utt_num = { 'all': 0}

for audio_corpus in audio_corpora:

    logging.info("exporting transcripts from %s ..." % audio_corpus)

    transcripts = Transcripts(corpus_name=audio_corpus)

    ts_all = transcripts.split()

    export_audio('all', ts_all)
    
    logging.info("exported transcripts from %s: %d samples." % (audio_corpus, len(ts_all)))

logging.info ( "All done." )

