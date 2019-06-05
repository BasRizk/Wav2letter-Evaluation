## update alternatives
update-alternatives --install /usr/lib/x86_64-linux-gnu/libblas.so     \
                    libblas.so-x86_64-linux-gnu      /home/$USER/intel/mkl/lib/intel64/libmkl_rt.so 50
update-alternatives --install /usr/lib/x86_64-linux-gnu/libblas.so.3   \
                    libblas.so.3-x86_64-linux-gnu    /home/$USER/intel/mkl/lib/intel64/libmkl_rt.so 50
update-alternatives --install /usr/lib/x86_64-linux-gnu/liblapack.so   \
                    liblapack.so-x86_64-linux-gnu    /home/$USER/intel/mkl/lib/intel64/libmkl_rt.so 50
update-alternatives --install /usr/lib/x86_64-linux-gnu/liblapack.so.3 \
                    liblapack.so.3-x86_64-linux-gnu  /home/$USER/intel/mkl/lib/intel64/libmkl_rt.so 50

echo "/home/$USER/intel/lib/intel64"     >  /etc/ld.so.conf.d/mkl.conf
echo "/home/$USER/intel/mkl/lib/intel64" >> /etc/ld.so.conf.d/mkl.conf
ldconfig


echo "Update Alternatives based on INTEL MKL installed in HOME"
