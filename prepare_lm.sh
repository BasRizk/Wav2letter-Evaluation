#!/usr/bin/env bash

# PREPARING GERMAN LM BY ZAMIA-SPEECH
GERMAN_MODEL_DIR=models/de
if [ ! -f "$GERMAN_MODEL_DIR/6_gram.arpa" ]; then
    wget --no-check-certificate https://goofy.zamia.org/zamia-speech/lm/generic_de_lang_model_large-r20190501.arpa.xz
    tar -xJf generic_de_lang_model_large-r20190501.arpa.xz
    # rm -f generic_de_lang_model_large-r20190501.arpa.xz
    mkdir -p $GERMAN_MODEL_DIR
    mv generic_de_lang_model_large-r20190501.arpa $GERMAN_MODEL_DIR/6_gram.arpa
else
    echo "German model 6_gram arpa file already exists."
fi

if [ ! -f "$GERMAN_MODEL_DIR/6_gram.binary" ]; then
    /home/$USER/wav2letter/kenlm/build/bin/build_binary -a 255 -q 8 trie $GERMAN_MODEL_DIR/6_gram.arpa $GERMAN_MODEL_DIR/6_gram.binary
else
    echo "German model 6_gram.binary file already exists."
fi


# PREPARING EN LM BY ZAMIA-SPEECH
ENGLISH_MODEL_DIR=models/en
if [ ! -f "$ENGLISH_MODEL_DIR/6_gram.arpa" ]; then
    wget --no-check-certificate https://goofy.zamia.org/zamia-speech/lm/generic_en_lang_model_large-r20190501.arpa.xz
    tar -xJf generic_en_lang_model_large-r20190501.arpa.xz
    # rm -f generic_en_lang_model_large-r20190501.arpa.xz
    mkdir -p $ENGLISH_MODEL_DIR
    mv generic_en_lang_model_large-r20190501.arpa.xz $ENGLISH_MODEL_DIR/6_gram.arpa
else
    echo "German model 6_gram arpa file already exists."
fi

if [ ! -f "$ENGLISH_MODEL_DIR/6_gram.binary" ]; then
    /home/$USER/wav2letter/kenlm/build/bin/build_binary -a 255 -q 8 trie $ENGLISH_MODEL_DIR/6_gram.arpa $ENGLISH_MODEL_DIR/6_gram.binary
else
    echo "English model 6_gram.binary file already exists."
fi

echo "Prepared En & De Large 6-gram lm models from Zamia-Speech"
