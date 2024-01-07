import os

bucket_choice = os.environ.get("S3_BUCKET")
bucket_options = {
    "default": "s3://gcorradini-forge-runner-test",
    "test": "s3://gcorradini-forge-runner-test"
}
s3_uri = bucket_options.get(bucket_choice)
if not s3_uri:
    raise ValueError(f"'S3_BUCKET_OPTIONS_MAP' did not have a key for '{bucket_choice}'. Options are {bucket_options}")

BUCKET_PREFIX = s3_uri
c.Bake.prune = bool(int(os.environ.get('PRUNE_OPTION')))
c.Bake.container_image = 'apache/beam_python3.10_sdk:2.52.0'
c.Bake.bakery_class = 'pangeo_forge_runner.bakery.flink.FlinkOperatorBakery'
c.Bake.feedstock_subdir = os.environ.get("FEEDSTOCK_SUBDIR")

c.FlinkOperatorBakery.parallelism = int(os.environ.get('PARALLELISM_OPTION'))
c.FlinkOperatorBakery.enable_job_archiving = True
c.FlinkOperatorBakery.flink_version = "1.16"
c.FlinkOperatorBakery.job_manager_resources = {"memory": "1536m", "cpu": 0.3}
c.FlinkOperatorBakery.task_manager_resources = {"memory": "3328m", "cpu": 0.3}
c.FlinkOperatorBakery.flink_configuration = {
    "taskmanager.numberOfTaskSlots": "1",
    "taskmanager.memory.flink.size": "2816m",
    "taskmanager.memory.task.heap.size": "1024m",
    "taskmanager.memory.task.off-heap.size": "256m"
}

c.TargetStorage.fsspec_class = "s3fs.S3FileSystem"
c.TargetStorage.root_path = f"{BUCKET_PREFIX}/{{job_name}}/output"
c.TargetStorage.fsspec_args = {
    "key": os.environ.get("S3_DEFAULT_AWS_ACCESS_KEY_ID"),
    "secret": os.environ.get("S3_DEFAULT_AWS_SECRET_ACCESS_KEY"),
    "client_kwargs": {"region_name": "us-west-2"}
}

c.InputCacheStorage.fsspec_class = c.TargetStorage.fsspec_class
c.InputCacheStorage.fsspec_args = c.TargetStorage.fsspec_args
c.InputCacheStorage.root_path = f"{BUCKET_PREFIX}/cache/{{job_name}}/input/"
