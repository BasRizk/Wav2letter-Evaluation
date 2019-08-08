export LD_LIBRARY_PATH=~/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin:/home/$USER/intel/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64_lin:/home/$USER/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin 

export CMAKE_LIBARY_PATH=~/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin:~/intel/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64_lin:~/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin

export MKLROOT=~/intel/mkl 

export MKL_ROOT=~/intel/mkl 

export KENLM_ROOT_DIR=~/wav2letter/kenlm 

#FEATURE_EXTRACTION ENV VARS -- PYTHON-BINDINGS
export LD_PRELOAD=~/intel/mkl/lib/intel64/libmkl_def.so:~/intel/mkl/lib/intel64/libmkl_avx2.so:~/intel/mkl/lib/intel64/libmkl_core.so:~/intel/mkl/lib/intel64/libmkl_intel_lp64.so:~/intel/mkl/lib/intel64/libmkl_intel_thread.so:~/intel/lib/intel64_lin/libiomp5.so

echo "Exporting based that INTEL MKL is in HOME directory."
