#DONT FORGET ADDING DECODER & TEST BINARIES TO PATH VARIABLE IN YOUR ENVIRONMENT
if [ -z $TEST_DIR ]
then
  echo "Export TEST_DIR first. example 'en-data/iisys' Or 'en-data/test-other' "
  echo "Export USE_GPU='ON' or 'OFF'"
else
  Test --flagsfile=test_en.cfg --test=$TEST_DIR && Decoder --flagsfile=decode_en.cfg --test=$TEST_DIR && python create_benchmark.py $TEST_DIR $USE_GPU

fi
