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
c.FlinkOperatorBakery.task_manager_resources = {"memory": "13312m", "cpu": 0.3}
c.FlinkOperatorBakery.flink_configuration = {
    "taskmanager.numberOfTaskSlots": "1",
    "taskmanager.memory.flink.size": "12800m",
    # illustration of Flink memory model: https://nightlies.apache.org/flink/flink-docs-release-1.10/ops/memory/mem_detail.html#overview

    # sum of configured:
    # Framework Heap Memory (128.000mb default) +
    # Framework Off-Heap Memory (128.000mb default) +
    # Managed Memory (defaults to fraction 0.4 of total flink memory) +
    # Network Memory (defaults to fraction 0.1 of total flink memory) +
    # Task Heap Memory (set below) +
    # Task Off-Heap Memory (set below)
    # has to be below configured
    # Total Flink Memory (set above)
    # so this quick math will give us equal amounts of heap/off-heap
    # (Total Flink Memory - ((0.1 * Total Flink Memory) + (0.4 * Total Flink Memory) + 128 + 128)) / 2
    "taskmanager.memory.task.heap.size": "5376m",
    "taskmanager.memory.framework.heap.size": "512m",
    "taskmanager.memory.task.off-heap.size": "256m",
    "taskmanager.memory.framework.off-heap.size": "256m",
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
