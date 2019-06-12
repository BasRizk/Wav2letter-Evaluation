#!/usr/bin/env bash

# PREPARING GERMAN MODEL BY ZAMIA-SPEECH
GERMAN_MODEL_DIR=models/de
if [ ! -d models/de ]
then
    wget --no-check-certificate http://goofy.zamia.org/zamia-speech/asr-models/w2l-generic-de-r20190427.tar.xz
    tar -xJf w2l-generic-de-r20190427.tar.xz
    rm -f w2l-generic-de-r20190427.tar.xz

    mkdir -p $GERMAN_MODEL_DIR
    mv w2l-generic-de-r20190427/README.md README-ZAMIA-DE-MODEL.md
    mv w2l-generic-de-r20190427/* $GERMAN_MODEL_DIR
    rm -rf w2l-generic-de-r20190427

    echo "Zamia-Speech W2L German Model is prepared."
else
    echo "Directory models/de does exist already!"
fi

wget --no-check-certificate https://goofy.zamia.org/zamia-speech/g2p/sequitur-dict-de.ipa-r20190113.gz
gunzip sequitur-dict-de.ipa-r20190113.gz
rm -f sequitur-dict-de.ipa-r20190113.gz
mv sequitur-dict-de.ipa-r20190113 $GERMAN_MODEL_DIR/dict-de.ipa

#TODO prepare own english model later.
