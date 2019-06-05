#!/usr/bin/env bash

# PREPARING GERMAN MODEL BY ZAMIA-SPEECH
wget --no-check-certificate http://goofy.zamia.org/zamia-speech/asr-models/w2l-generic-de-r20190427.tar.xz
tar -xJf w2l-generic-de-r20190427.tar.xz
rm -f w2l-generic-de-r20190427.tar.xz

GERMAN_MODEL_DIR=models/de
mkdir -p $GERMAN_MODEL_DIR
mv w2l-generic-de-r20190427/README.md README-ZAMIA-DE-MODEL.md
mv w2l-generic-de-r20190427/* $GERMAN_MODEL_DIR
rm -rf w2l-generic-de-r20190427

echo "Zamia-Speech W2L German Model is prepared."

#TODO prepare own english model later.
