PREFIX_HERE=/opt/intel

export LD_LIBRARY_PATH=$PREFIX_HERE/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin:$PREFIX_HERE/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64_lin:$PREFIX_HERE/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin 

export CMAKE_LIBARY_PATH=$PREFIX_HERE/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin:$PREFIX_HERE/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64_lin:$PREFIX_HERE/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin

export MKLROOT=$PREFIX_HERE/mkl

export MKL_ROOT=$PREFIX_HERE/mkl

export KENLM_ROOT_DIR=~/wav2letter/kenlm

echo "Exporting based that INTEL MKL is in OPT directory."
