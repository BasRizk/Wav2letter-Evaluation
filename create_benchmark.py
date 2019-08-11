# -*- coding: utf-8 -*-
from os import path, makedirs, listdir
from utils import cpu_info, gpu_info, prepare_pathes
from jiwer import wer  
from os.path import join, realpath
import platform
import soundfile as sf
import pandas as pd  
import time
import shutil



IS_RECURSIVE_DIRECTORIES = True
IS_TSV = False
USING_GPU = False
if USING_GPU:
    print("Using GPU support.\n")
VERBOSE = True

import sys
if sys.argv[1] == "en-data/iisys":
    TEST_PATH = "tests/iisys"
else:
    TEST_PATH = "tests/LibriSpeech/test-other"

print("TEST_PATH:" + TEST_PATH + "\n")

TEST_PATH_POSTFIX = TEST_PATH.split("/")[-1]
SYM_TEST_PATH = path.join("tests/en-data", TEST_PATH_POSTFIX)
hypothesis_file = "logs/en-data#" + TEST_PATH_POSTFIX + ".hyp"

DECODE_LOG_PATH = "decode_log.txt"
TEST_LOG_PATH = "test_log.txt"
assert(path.exists(TEST_PATH))

try:
    TEST_CORPUS = TEST_PATH.split("/")[1]
except:
    print("WARNING: Path 2nd index does not exist.\n")

if  TEST_CORPUS == "iisys":
    IS_TSV = True
    IS_RECURSIVE_DIRECTORIES = False
    ORG_AUDIO_INPUT = "wav"
else:
    IS_TSV = False
    IS_RECURSIVE_DIRECTORIES = True
    ORG_AUDIO_INPUT = "flac"


try:
    if TEST_PATH.split("/")[2] == "Sprecher":
        AUDIO_INPUT="flac"
except:
    print("WARNING: Path 3rd index does not exist.\n")

# =============================================================================
# ------------------------Documenting Machine ID
# =============================================================================
localtime = time.strftime("%Y%m%d-%H%M%S")
platform_id = platform.machine() + "_" + platform.system() + "_" +\
                platform.node() + "_" + localtime
                
                
if USING_GPU:
    platform_id += "_use_gpu"

if TEST_CORPUS:
    platform_id = TEST_CORPUS + "_" + platform_id

platform_meta_path = "logs/online/" + platform_id

if not path.exists(platform_meta_path):
    makedirs(platform_meta_path)

if(USING_GPU):
    with open(join(platform_meta_path,"gpu_info.txt"), 'w') as f:
        f.write(gpu_info())
else:
    with open(join(platform_meta_path,"cpu_info.txt"), 'w') as f:
        f.write(cpu_info())

# =============================================================================
# ------------------------------Preparing pathes
# =============================================================================
log_filepath = platform_meta_path  +"/logs_" + localtime + ".txt"
summ_filepath = platform_meta_path  +"/summ_" + localtime + ".txt"
benchmark_filepath = platform_meta_path  +"/w2l_benchmark_ " + localtime + ".csv"

test_log = pd.read_csv("test_log.txt", sep=",", skiprows=[0], header=None)
decode_log = pd.read_csv("decode_log.txt", sep=",", skiprows=[0], header=None)
result_log = open(hypothesis_file, "r")
                  
test_directories = prepare_pathes(TEST_PATH, recursive = IS_RECURSIVE_DIRECTORIES)
text_pathes = list()
text_file_exten = "txt"
if IS_TSV:
    text_file_exten = "tsv"
for d in test_directories:
    text_pathes.append(prepare_pathes(d, text_file_exten, recursive = False))
text_pathes.sort()  

# =============================================================================
# ---Running the Kaldi STT Engine by running through the audio files
# =============================================================================

log_file = open(log_filepath, "w")
summ_file = open(summ_filepath, "w")

def extend_name(filename, num_chars, extension, filler="0"):
    filename = str(filename)
    filename = filler*(num_chars - len(filename)) + filename
    return filename + "." + extension

processed_data = "filename,length(sec),proc_time(sec),wer,actual_text,processed_text\n"
avg_wer = 0
avg_proc_time = 0
avg_proc_time_inc_save = 0
current_audio_number = 1

text_pathes = [path for subpathes in text_pathes for path in subpathes]

if IS_TSV:
    audio_transcripts = pd.concat( [ pd.read_csv(text_path, sep='\t', header=None, engine='python') for text_path in text_pathes] )
    audio_transcripts.sort_values(by = 0)
else:
    audio_transcripts = pd.concat( [ pd.read_csv(text_path, header=None, engine='python') for text_path in text_pathes] )
    audio_transcripts.sort_values(by = 0)
    audio_transcripts = audio_transcripts[0].str.split(" ", 1, expand = True)
audio_transcripts[1] = audio_transcripts[1].str.lower()
audio_transcripts = audio_transcripts.set_index(0)[1].to_dict()

benchmark = pd.DataFrame(columns=["filename","length(sec)","proc_time(sec)", "wer", "actual_text", "processed_text", "proc_time(sec - includes emission save time)"])

num_of_audiofiles  = 0
for inf_time, inf_save_time, sample_id_test, dec_time, sample_id_decode, result_line \
                in zip(test_log[0], test_log[1], test_log[2],
                       decode_log[0], decode_log[1], result_log):
    #print(inf_time, inf_save_time, sample_id_test, dec_time, sample_id_decode)
    if sample_id_test == sample_id_decode:
        sample_id = sample_id_test
    audio_path = realpath(join(SYM_TEST_PATH, extend_name(sample_id, 9, ORG_AUDIO_INPUT)))

    try:
        audio, fs = sf.read(audio_path, dtype='int16')
    except:
        if VERBOSE: 
            print("# WARNING :: Audio File" + audio_path + " not readable.\n")
        log_file.write("# WARNING :: Audio File " + audio_path + " not readable.\n")
        continue
    
    audio_len = len(audio)/fs 
    print('Inference took (%0.3fs + %0.3fs) for %0.3fs audio file.\n' % (inf_time, dec_time, audio_len))
    inf_time = round(inf_time,3)
    inf_inc_save_time = round(inf_save_time,3)
    dec_time = round(dec_time,3)
    proc_time = inf_time + dec_time
    proc_time_inc_inf_save = inf_inc_save_time + dec_time
    
    # Processing WORD ERROR RATE (WER)
    processed_text = " ".join(result_line.split(" ")[:-1])
    audio_filename = audio_path.split("/")[-1].split(".")[0]
    actual_text = audio_transcripts.get(audio_filename)
    if not actual_text:
        if VERBOSE: 
            print("# WARNING :: Transcript of file " + audio_filename + " does not exist.\n")
        log_file.write("# WARNING :: Transcript of file " + audio_filename + " does not exist.\n")
        continue
    
    num_of_audiofiles +=1
    current_wer = wer(actual_text, processed_text, standardize=True)
    current_wer = round(current_wer,3)
    
    # Accumlated data
    avg_proc_time += (proc_time/audio_len)
    avg_proc_time_inc_save += (proc_time_inc_inf_save/audio_len)
    avg_wer += current_wer
    
    audio_path = audio_path.split("/")[-1]
    progress_row = audio_path + "," + str(audio_len) + "," + str(proc_time)  + "," +\
                    str(current_wer) + "," + actual_text + "," + processed_text
    
    num_of_audiofiles+=1
    benchmark.append([audio_filename, audio_len, proc_time, current_wer,
                      actual_text, processed_text, proc_time_inc_inf_save], ignore_index=False)
   
    if(VERBOSE):
        print("# Audio number " + str(num_of_audiofiles) + "\n" +\
		  "# File (" + audio_path + "):\n" +\
              "# - " + str(audio_len) + " seconds long.\n"+\
              "# - actual    text: '" + actual_text + "'\n" +\
              "# - processed text: '" + processed_text + "'\n" +\
              "# - processed in "  + str(proc_time) + " seconds.\n"
              "# - WER = "  + str(current_wer) + "\n")
              
    log_file.write("# Audio number " + str(num_of_audiofiles) + "\n" +\
	      "# File (" + audio_path + "):\n" +\
          "# - " + str(audio_len) + " seconds long.\n"+\
          "# - actual    text: '" + actual_text + "'\n" +\
          "# - processed text: '" + processed_text + "'\n" +\
          "# - processed in "  + str(proc_time) + " seconds.\n"
          "# - WER = "  + str(current_wer) + "\n")
    
              
    processed_data+= progress_row + "\n"

# =============================================================================
# ---------------Finalizing processed data and Saving Logs
# =============================================================================

avg_proc_time /= num_of_audiofiles
avg_proc_time_inc_save /= num_of_audiofiles
avg_wer /= num_of_audiofiles
if(VERBOSE):
    print("Avg. Proc. time (sec/second of audio) = " + str(avg_proc_time) + "\n" +\
          "Avg. Proc. time inc. SAVE (sec/second of audio) = " + str(avg_proc_time_inc_save) + "\n" +\
          "Avg. WER = " + str(avg_wer))
log_file.write("Avg. Proc. time/sec = " + str(avg_proc_time) + "\n" +\
          "Avg. Proc. time inc. SAVE (sec/second of audio) = " + str(avg_proc_time_inc_save) + "\n" +\
          "Avg. WER = " + str(avg_wer))
summ_file.write("Avg. Proc. time/sec," + str(avg_proc_time) + "\n" +\
          "Avg. Proc. time inc. SAVE (sec/second of audio) = " + str(avg_proc_time_inc_save) + "\n" +\
          "Avg. WER," + str(avg_wer))
log_file.close()
summ_file.close()

processed_data+= "AvgProcTime (sec/second of audio)," + str(avg_proc_time) + "\n"
processed_data+= "Avg. Proc. time inc. SAVE (sec/second of audio) = " + str(avg_proc_time_inc_save) + "\n"
processed_data+= "AvgWER," + str(avg_wer) + "\n"


with open(benchmark_filepath, 'w') as f:
    for line in processed_data:
        f.write(line)

# =============================================================================
# ---------------CLEAN UP
# =============================================================================
print("About to move all files relating to specific log directory...\n")
def move_to_specific_log(old_file, new_file=None):
    if new_file == None:
        new_file = path.join(platform_meta_path, old_file)
    shutil.move(old_file, new_file)

for file in listdir("logs"):
    if "en-data" in file:
        old_file = path.join("logs", file)
        new_file = path.join(platform_meta_path, file)
        move_to_specific_log(old_file, new_file)
print("=> Main logs moved to specific dir.\n")

move_to_specific_log("test_log.txt")
move_to_specific_log("decode_log.txt")
print("=> Eval logs moved to specific dir.\n")






