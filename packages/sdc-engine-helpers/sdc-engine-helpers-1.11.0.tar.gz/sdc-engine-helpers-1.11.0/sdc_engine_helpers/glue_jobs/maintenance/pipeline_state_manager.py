"""
    Pipeline state manager module
"""
from datetime import datetime
import sdc_helpers.utils as utils
import boto3
from sdc_engine_helpers.date_utils import DateUtils


class PipelineStateManager:
    """
        Given a database pipeline object, check whether it should be executed
    """
    date_utils = None
    glue = None

    def __init__(self):
        self.date_utils = DateUtils()
        self.glue = boto3.client('glue')

    def get_state(self, *, pipeline: dict) -> dict:
        """
            Get the current state of the pipeline

            args:
                pipeline (dict): Pipeline from the database

            returns:
                state (dict): Dictionary containing:
                    1) should_execute
                    2) next_execution_at (if frequency specified)

        """
        state = {
            'should_execute': False,
            'next_execution_at': None
        }

        glue_job_run = None
        job_run_id = pipeline.get('job_run_id', None)
        if job_run_id is not None:
            glue_job_run = self.glue.get_job_run(
                JobName=pipeline.get('job_name'),
                RunId=job_run_id
            )

        state['should_execute'] = self.should_execute(
            pipeline=pipeline,
            glue_job_run=glue_job_run
        )

        if state['should_execute']:
            this_execution_time = pipeline.get('next_execution_at', None)
            frequency = pipeline.get('frequency', None)

            if frequency:
                state['next_execution_at'] = self.date_utils.get_next_time(
                    this_time=this_execution_time,
                    frequency=frequency
                )

        return state

    @staticmethod
    def should_execute(
            *,
            pipeline: dict,
            glue_job_run
    ) -> bool:
        """
            Check whether a pipeline should execute when all of the following are true:

            1) The last job run state is STOPPED or SUCCEEDED
            2) The current time is >= the scheduled next execution time (if specified)

            args:
                pipeline (dict): Pipeline from the database
                glue_job_run (dict/None): Glue job dictionary

            returns:
                result (bool): Should execute

        """
        if (
                glue_job_run is not None and
                utils.dict_query(
                    dictionary=glue_job_run,
                    path='JobRun.JobRunState'
                ) not in ['STOPPED', 'SUCCEEDED', 'FAILED']
        ):
            return False

        frequency = pipeline.get('frequency', None)

        if frequency:
            next_execution_at = pipeline.get('next_execution_at')
            if next_execution_at:
                if (
                        datetime.now() <
                        datetime.strptime(next_execution_at, "%Y-%m-%d %H:%M:%S")
                ):
                    return False

        return True
