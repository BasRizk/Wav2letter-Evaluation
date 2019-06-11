#!/usr/bin/env bash

# PREPARING ENGLISH LIBRISPEECH CLEAN-TEST DATASET
W2L_TEST_DIR=tests
W2L_DE_TEST_DIR=$W2L_TEST_DIR/data-de
mkdir -p $W2L_DE_TEST_DIR
wget -qO- https://goofy.zamia.org/zamia-speech/corpora/forschergeist/timpritlove-20180320-rec.tgz | tar xvz -C $W2L_TEST_DIR
python prepare_zamia_german_data.py --src $W2L_TEST_DIR/timpritlove-20180320-rec/ --dst $W2L_DE_TEST_DIR
echo "Finished preparing Zamia timpritlove-20180320-rec dataset"

