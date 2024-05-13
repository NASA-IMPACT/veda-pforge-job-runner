import argparse
import datetime

import boto3
import json
import time
from uuid import uuid4
from tenacity import retry, stop_after_delay, wait_exponential
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = boto3.client('emr-serverless')


@retry(wait=wait_exponential(multiplier=1, max=60), stop=stop_after_delay(300))
def block_on_app_state(application_id):
    resp = client.get_application(applicationId=application_id)
    if resp.get('application').get('state') != 'STARTED':
        logger.debug("retrying...")
        raise Exception("retrying...")
    else:
        # even after reaching STARTED state sometimes SubmitJobRun seems to fail
        time.sleep(10)
        logger.debug("Application has started and we can submit the job now")


@retry(wait=wait_exponential(multiplier=1, max=60), stop=stop_after_delay(300))
def block_on_job_state(application_id, job_id):
    resp = client.get_job_run(applicationId=application_id, jobRunId=job_id)
    if resp.get('jobRun').get('state') != 'RUNNING':
        logger.debug("retrying...")
        raise Exception("retrying...")
    else:
        time.sleep(10)
        logger.debug("Job is RUNNING and we can get dashboard URL now")


def start_emr_job(application_id, execution_role_arn, entry_point, entry_point_arguments, spark_submit_params, configuration_overrides, tags, execution_timeout, name):

    job_driver = {
        'sparkSubmit': {
            'entryPoint': entry_point,
            'entryPointArguments': entry_point_arguments.split(),
            'sparkSubmitParameters': spark_submit_params
        }
    }

    client.start_application(applicationId=application_id)
    block_on_app_state(application_id)

    idempotency_token = str(uuid4())
    response = client.start_job_run(
        applicationId=application_id,
        clientToken=idempotency_token,
        executionRoleArn=execution_role_arn,
        jobDriver=job_driver,
        configurationOverrides=configuration_overrides,
        tags=tags,
        executionTimeoutMinutes=execution_timeout,
        name=name
    )
    return response


def get_job_run_url(application_id):
    created_after = datetime.datetime.now() - datetime.timedelta(minutes=5)
    job_runs = client.list_job_runs(
        applicationId=application_id,
        maxResults=5,
        createdAtAfter=created_after,
    )

    if len(job_runs['jobRuns']) > 0:
        sorted_job_runs = sorted(job_runs['jobRuns'], key=lambda x: x["createdAt"], reverse=True)
        job_id = sorted_job_runs[0]['id']
        logger.debug(f"[ JOB ID ]: {job_id}")

        block_on_job_state(application_id, job_id)

        job_run = client.get_dashboard_for_job_run(
            applicationId=application_id,
            jobRunId=job_id
        )
        logger.debug(f"[ DASHBOARD URL ]: {job_run}")
    else:
        logger.debug(f"No job runs found createdAtAfter={created_after}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a Spark job on EMR Serverless.')

    parser.add_argument('--application-id', required=True, help='Application ID for the EMR Serverless application')
    parser.add_argument('--execution-role-arn', required=True, help='Execution role ARN')
    parser.add_argument('--entry-point', required=True, help='Entry point for the Spark job (e.g., s3://bucket/script.py)')
    parser.add_argument('--entry-point-arguments', default='', help='Space-separated entry point arguments')
    parser.add_argument('--spark-submit-parameters', default='', help='Spark submit parameters')
    parser.add_argument('--configuration-overrides', type=json.loads, default={}, help='JSON string for configuration overrides')
    parser.add_argument('--tags', type=json.loads, default={}, help='JSON string for tags')
    parser.add_argument('--execution-timeout', type=int, default=123, help='Execution timeout in minutes')
    parser.add_argument('--name', required=True, help='Name for the job run')
    parser.add_argument('--workflow', type=str, default="startjob", help='which workflow to run startjob or getjob')

    args = parser.parse_args()

    if args.workflow == "startjob":
        response = start_emr_job(
            application_id=args.application_id,
            execution_role_arn=args.execution_role_arn,
            entry_point=args.entry_point,
            entry_point_arguments=args.entry_point_arguments,
            spark_submit_params=args.spark_submit_parameters,
            configuration_overrides=args.configuration_overrides,
            tags=args.tags,
            execution_timeout=args.execution_timeout,
            name=args.name
        )

        logger.debug("Job started successfully. Response:")
        logger.debug(response)
    elif args.workflow == "getjob":
        get_job_run_url(args.application_id)
