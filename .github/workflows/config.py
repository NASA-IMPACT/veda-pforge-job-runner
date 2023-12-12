import os

# TODO handle bucket choices here based on inputs

BUCKET_PREFIX = os.environ.get("S3_BUCKET", "s3://gcorradini-forge-runner-test")
c.Bake.prune = bool(os.environ.get('PRUNE_OPTION', 'False'))
c.Bake.container_image = 'apache/beam_python3.10_sdk:2.52.0'
c.Bake.bakery_class = "pangeo_forge_runner.bakery.flink.FlinkOperatorBakery"

c.FlinkOperatorBakery.parallelism = int(os.environ.get('PARALLELISM_OPTION', '1'))
c.FlinkOperatorBakery.enable_job_archiving = True
c.FlinkOperatorBakery.flink_version = "1.16"
c.FlinkOperatorBakery.job_manager_resources = {"memory": "1536m", "cpu": 0.5}
c.FlinkOperatorBakery.task_manager_resources = {"memory": "1536m", "cpu": 0.5}
c.FlinkOperatorBakery.flink_configuration= {
   "taskmanager.numberOfTaskSlots": "1",
   "taskmanager.memory.flink.size": "1280m",
}

c.TargetStorage.fsspec_class = "s3fs.S3FileSystem"
c.TargetStorage.root_path = f"{BUCKET_PREFIX}/{{job_name}}/output"
c.TargetStorage.fsspec_args = {
    "key": os.environ.get("S3_DEFAULT_AWS_ACCESS_KEY_ID"),
    "secret": os.environ.get("S3_DEFAULT_AWS_SECRET_ACCESS_KEY"),
    "client_kwargs":{"region_name":"us-west-2"}
}

c.InputCacheStorage.fsspec_class = c.TargetStorage.fsspec_class
c.InputCacheStorage.fsspec_args = c.TargetStorage.fsspec_args
c.InputCacheStorage.root_path = f"{BUCKET_PREFIX}/cache/{{job_name}}/input/"