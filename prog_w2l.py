# -*- coding: utf-8 -*-


import math
import os
import struct
import sys

import itertools as it
from wav2letter.feature import FeatureParams, Mfcc

import torch
from wav2letter.criterion import ASGLoss, CriterionScaleMode

import flashlight as fl
model = fl.FlashLight("models/en/am/007_model_librispeech-full#data#valid.bin")
                      
import numpy as np
from wav2letter.common import Dictionary, createWordDict, loadWords, tkn2Idx
from wav2letter.decoder import (
    CriterionType,
    DecoderOptions,
    KenLM,
    SmearingMode,
    Trie,
    WordLMDecoder,
)

mfcc_config_path = "/home/ironbas7/wav2letter/wav2letter/src/feature/test/data"
testing_data_path = "/home/ironbas7/wav2letter/wav2letter/src/decoder/test"
data_path = "tests/en-data/data/test-other"
model_path = "models/en"
#model = torch.load("models/en/am/007_model_librispeech-full#data#valid.bin")

########

import soundfile as sf

wavinput, _ = sf.read(os.path.join(data_path, "000000000.wav"))

assert len(wavinput) > 0

params = FeatureParams()
params.samplingFreq = 160
params.lowFreqFilterbank = 0
params.highFreqFilterbank = 8000
params.zeroMeanFrame = True
params.numFilterbankChans = 20
params.numCepstralCoeffs = 13
params.useEnergy = False
params.zeroMeanFrame = False
params.usePower = False
#
#mfcc = Mfcc(params)
#feat = mfcc.apply(wavinput)
#
#assert len(feat) % 39 == 0
#numframes = len(feat) // 39
#featcopy = feat.copy()
#for f in range(numframes):
#    for i in range(1, 39):
#        feat[f * 39 + i - 1] = feat[f * 39 + i]
#    feat[f * 39 + 12] = featcopy[f * 39 + 0]
#    feat[f * 39 + 25] = featcopy[f * 39 + 13]
#    feat[f * 39 + 38] = featcopy[f * 39 + 26]
#
#print("featcopy", featcopy)
#print("numframes", numframes)


########

#!/usr/bin/env python3


USING_GPU = False

device = torch.device("cpu" if not USING_GPU else "cuda")
asg = ASGLoss(6, scale_mode=CriterionScaleMode.TARGET_SZ_SQRT).to(device)
input = torch.tensor(
    [
        [
            [-0.4340, -0.0254, 0.3667, 0.4180, -0.3805, -0.1707],
            [0.1060, 0.3631, -0.1122, -0.3825, -0.0031, -0.3801],
            [0.0443, -0.3795, 0.3194, -0.3130, 0.0094, 0.1560],
            [0.1252, 0.2877, 0.1997, -0.4554, 0.2774, -0.2526],
            [-0.4001, -0.2402, 0.1295, 0.0172, 0.1805, -0.3299],
        ],
        [
            [0.3298, -0.2259, -0.0959, 0.4909, 0.2996, -0.2543],
            [-0.2863, 0.3239, -0.3988, 0.0732, -0.2107, -0.4739],
            [-0.0906, 0.0480, -0.1301, 0.3975, -0.3317, -0.1967],
            [0.4372, -0.2006, 0.0094, 0.3281, 0.1873, -0.2945],
            [0.2399, 0.0320, -0.3768, -0.2849, -0.2248, 0.3186],
        ],
        [
            [0.0225, -0.3867, -0.1929, -0.2904, -0.4958, -0.2533],
            [0.4001, -0.1517, -0.2799, -0.2915, 0.4198, 0.4506],
            [0.1446, -0.4753, -0.0711, 0.2876, -0.1851, -0.1066],
            [0.2081, -0.1190, -0.3902, -0.1668, 0.1911, -0.2848],
            [-0.3846, 0.1175, 0.1052, 0.2172, -0.0362, 0.3055],
        ],
    ],
    dtype=torch.float,
    device=device,
    requires_grad=True,
)
target = torch.tensor(
    [[2, 1, 5, 1, 3], [4, 3, 5, -1, -1], [3, 2, 2, 1, -1]],
    dtype=torch.int,
    device=device,
)
target_size = torch.tensor([5, 3, 4], dtype=torch.int, device=device)
grad = torch.ones(3, dtype=torch.float, device=device)

print(list(asg.parameters()))
loss = asg.forward(input, target, target_size)
print(loss)
loss.backward(grad)
print(input.grad)
print(asg.trans.grad)

########
def read_struct(file, fmt):
    return struct.unpack(fmt, file.read(struct.calcsize(fmt)))


def load_TN(path):
    with open(path, "rb") as file:
        T = read_struct(file, "i")[0]
        N = read_struct(file, "i")[0]
        return T, N


def load_emissions(path):
    with open(path, "rb") as file:
        return np.frombuffer(file.read(T * N * 4), dtype=np.float32)


def load_transitions(path):
    with open(path, "rb") as file:
        return np.frombuffer(file.read(N * N * 4), dtype=np.float32)


def assert_near(x, y, tol):
    assert abs(x - y) <= tol



# load test files

T, N = load_TN(os.path.join(testing_data_path, "TN.bin"))
emissions = load_emissions(os.path.join(testing_data_path, "emission.bin"))
transitions = load_transitions(os.path.join(testing_data_path, "transition.bin"))
lexicon = loadWords(os.path.join(testing_data_path, "words.lst"))
wordDict = createWordDict(lexicon)
tokenDict = Dictionary(os.path.join(testing_data_path, "letters.lst"))
tokenDict.addEntry("1")
lm = KenLM(os.path.join(testing_data_path, "lm.arpa"), wordDict)

# test LM

#sentence = ["the", "cat", "sat", "on", "the", "mat"]
#lm_state = lm.start(False)
#total_score = 0
#lm_score_target = [-1.05971, -4.19448, -3.33383, -2.76726, -1.16237, -4.64589]
#for i in range(len(sentence)):
#    lm_state, lm_score = lm.score(lm_state, wordDict.getIndex(sentence[i]))
#    assert_near(lm_score, lm_score_target[i], 1e-5)
#    total_score += lm_score
#lm_state, lm_score = lm.finish(lm_state)
#total_score += lm_score
#assert_near(total_score, -19.5123, 1e-5)

# build trie
sentence = ["the", "cat", "sat", "on", "the", "mat"]
sil_idx = tokenDict.getIndex("|")
unk_idx = wordDict.getIndex("<unk>")
trie = Trie(tokenDict.indexSize(), sil_idx)
start_state = lm.start(False)

for word, spellings in lexicon.items():
    usr_idx = wordDict.getIndex(word)
    _, score = lm.score(start_state, usr_idx)
    for spelling in spellings:
        # maxReps should be 1; using 0 here to match DecoderTest bug
        spelling_idxs = tkn2Idx(spelling, tokenDict, 0)
        trie.insert(spelling_idxs, usr_idx, score)

trie.smear(SmearingMode.MAX)

trie_score_target = [-1.05971, -2.87742, -2.64553, -3.05081, -1.05971, -3.08968]
for i in range(len(sentence)):
    word = sentence[i]
    # maxReps should be 1; using 0 here to match DecoderTest bug
    word_tensor = tkn2Idx([c for c in word], tokenDict, 0)
    node = trie.search(word_tensor)
    assert_near(node.maxScore, trie_score_target[i], 1e-5)

beamSize = 2500
beamThreshold = 100.0
lmWeight = 2.0
wordScore = 2.0
unkScore = -math.inf
logAdd = False
silWeight = -1
criterionType = CriterionType.ASG

opts = DecoderOptions(beamSize,
                      beamThreshold,
                      lmWeight,
                      wordScore,
                      unkScore,
                      logAdd,
                      silWeight,
                      criterionType)

decoder = WordLMDecoder(opts, trie, lm, sil_idx, -1, unk_idx, transitions)
results = decoder.decode(emissions.ctypes.data, T, N)

print(f"Decoding complete, obtained {len(results)} results")
print("Showing top 5 results:")
for i in range(5):
    prediction = []
    for idx in results[i].tokens:
        if idx < 0:
            break
        prediction.append(tokenDict.getEntry(idx))
    prediction = " ".join(prediction)
    print(f"score={results[i].score} prediction='{prediction}'")

assert len(results) == 1452
hyp_score_target = [-278.111, -278.652, -279.275, -279.847, -280.01]
for i in range(5):
    assert_near(results[i].score, hyp_score_target[i], 1e-3)
