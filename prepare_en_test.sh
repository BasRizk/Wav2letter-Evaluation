#!/usr/bin/env bash

# PREPARING ENGLISH LIBRISPEECH CLEAN-TEST DATASET
W2L_TEST_DIR=tests
W2L_EN_TEST_DIR=$W2L_TEST_DIR/en-data

if [ ! -d $W2L_TEST_DIR/LibriSpeech ]; then
  mkdir -p $W2L_EN_TEST_DIR
  wget -qO- http://www.openslr.org/resources/12/test-other.tar.gz | tar xvz -C $W2L_TEST_DIR
fi

python prepare_librispeech_data.py --src $W2L_TEST_DIR/LibriSpeech/ --dst $W2L_EN_TEST_DIR
python prepare_lexicon.py
echo "Finished preparing LibriSpeech Clean-Test dataset"

