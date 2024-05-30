FROM public.ecr.aws/emr-serverless/spark/emr-7.0.0:latest

USER root
WORKDIR /opt


# Update and install required packages
RUN dnf update -y && \
    dnf install -y \
    git \
    gcc \
    gcc-c++ \
    make \
    wget \
    zlib-devel \
    python3-devel && \
    dnf clean all


# Download and build HDF5 from source with thread safety and parallel enabled
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.14/hdf5-1.14.3/src/hdf5-1.14.3.tar.gz && \
    tar -xzf hdf5-1.14.3.tar.gz && \
    cd hdf5-1.14.3 && \
    ./configure --prefix=/usr --disable-fortran --enable-hl --with-zlib=/usr/include,/usr/lib && \
    make -j -l6 && \
    make install && \
    cd .. && \
    rm -rf hdf5-1.14.3 hdf5-1.14.3.tar.gz

# Set the HDF5 library path
ENV HDF5_DIR=/usr
ENV LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
ENV CPATH=/usr/include:$CPATH

# Install Python packages
RUN pip3 install \
  s3fs \
  gcsfs \
  boto3 \
  requests \
  apache-beam==2.53.0 \
  xarray==2024.1.1 \
  zarr==2.16.1 \
  venvception>=0.0.5 \
  jupyter-repo2docker \
  pangeo-forge-recipes \
  git+https://github.com/ranchodeluxe/beam-pyspark-runner@patch-2 \
  h5py \
  netcdf4 \
  wheel && \
  HDF5_DIR=/usr pip3 install --no-binary=h5py h5py

WORKDIR /home/hadoop
USER hadoop:hadoop