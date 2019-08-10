#DONT FORGET ADDING DECODER & TEST BINARIES TO PATH VARIABLE IN YOUR ENVIRONMENT
if [ -z $TEST_DIR ]
then
  echo "Export TEST_DIR first. example 'en-data/iisys' "
else
  Test --flagsfile=test_en.cfg --test=$TEST_DIR && Decoder --flagsfile=decode_en.cfg --test=$TEST_DIR
fi
