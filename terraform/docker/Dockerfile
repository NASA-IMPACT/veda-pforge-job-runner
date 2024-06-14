FROM public.ecr.aws/emr-serverless/spark/emr-7.0.0:latest

USER root
WORKDIR /opt

RUN yum update -y && yum install -y git

# TODO: none of this should declared in the image
# or in the runner image it should all be part
# of the recipe requirements.txt but we still
# need to solve
# https://github.com/NASA-IMPACT/veda-pforge-job-runner/pull/64
RUN pip3 install \
 git+https://github.com/ranchodeluxe/s3fs@gc/fetch_sync \
 gcsfs \
 boto3 \
 requests \
 apache-beam==2.53.0 \
 rioxarray \
 xarray==2024.1.1 \
 zarr==2.16.1 \
 venvception>=0.0.5 \
 jupyter-repo2docker \
 git+https://github.com/ranchodeluxe/beam-pyspark-runner@patch-2 \
 git+https://github.com/carbonplan/pangeo-forge-ndpyramid@main \
 git+https://github.com/pangeo-forge/pangeo-forge-recipes@s3fssync_support \
 httpfs_sync


WORKDIR /home/hadoop
USER hadoop:hadoop
