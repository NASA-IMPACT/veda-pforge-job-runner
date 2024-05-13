FROM public.ecr.aws/emr-serverless/spark/emr-7.0.0:latest

USER root
WORKDIR /opt

RUN yum update -y && yum install -y git

#RUN pip3 install \
#  s3fs \
#  gcsfs \
#  boto3 \
#  requests \
#  apache-beam==2.53.0 \
#  xarray==2024.1.1 \
#  zarr==2.16.1 \
#  venvception>=0.0.5 \
#  jupyter-repo2docker \
#  pangeo-forge-recipes \
#  git+https://github.com/ranchodeluxe/beam-pyspark-runner@patch-2

RUN pip3 install \
    git+https://github.com/moradology/venvception@ranchodeluxe-patch-1 \
    jupyter-repo2docker \
    git+https://github.com/ranchodeluxe/beam-pyspark-runner@patch-2

WORKDIR /home/hadoop
USER hadoop:hadoop
