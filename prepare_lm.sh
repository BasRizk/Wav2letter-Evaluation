#!/usr/bin/env bash

# PREPARING GERMAN LM BY ZAMIA-SPEECH
wget --no-check-certificate https://goofy.zamia.org/zamia-speech/lm/generic_de_lang_model_large-r20190501.arpa.xz
tar -xJf generic_de_lang_model_large-r20190501.arpa.xz
# rm -f generic_de_lang_model_large-r20190501.arpa.xz

GERMAN_MODEL_DIR=models/de
mkdir -p $GERMAN_MODEL_DIR
mv generic_de_lang_model_large-r20190501.arpa $GERMAN_MODEL_DIR/6_gram.arpa

# PREPARING EN LM BY ZAMIA-SPEECH
wget --no-check-certificate https://goofy.zamia.org/zamia-speech/lm/generic_en_lang_model_large-r20190501.arpa.xz
tar -xJf generic_en_lang_model_large-r20190501.arpa.xz
# rm -f generic_en_lang_model_large-r20190501.arpa.xz

ENGLISH_MODEL_DIR=models/en
mkdir -p $ENGLISH_MODEL_DIR
mv generic_en_lang_model_large-r20190501.arpa.xz $ENGLISH_MODEL_DIR/6_gram.arpa

echo "Prepared En & De Large 6-gram lm models from Zamia-Speech"

# TODO convert models to binary for quicker 
