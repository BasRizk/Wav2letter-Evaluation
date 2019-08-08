#!/usr/bin/env bash

# PREPARING ENGLISH LIBRISPEECH CLEAN-TEST DATASET
W2L_TEST_DIR=tests
W2L_DE_TEST_DIR=$W2L_TEST_DIR/data-de
mkdir -p $W2L_TEST_DIR/forschergeist
wget -nc https://goofy.zamia.org/zamia-speech/corpora/forschergeist/timpritlove-20180320-rec.tgz & tar -xvzf timpritlove-20180320-rec.tgz -C $W2L_TEST_DIR/forschergeist
wget -nc https://goofy.zamia.org/zamia-speech/corpora/forschergeist/annettevogt-20180320-rec.tgz & tar -xvzf annettevogt-20180320-rec.tgz -C $W2L_TEST_DIR/forschergeist
python wav2letter_export_testonly.py -l de dict-de.ipa forschergeist
echo "Finished preparing Zamia timpritlove-20180320-rec dataset"

