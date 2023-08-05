"""
    Maintenance manager module
"""
from datetime import datetime
import json
from sdc_helpers.models.client import Client
import boto3
from sqlalchemy.exc import SQLAlchemyError
from sdc_engine_helpers import decorators
from sdc_engine_helpers.date_utils import DateUtils
from sdc_engine_helpers.glue_jobs.maintenance.pipeline_state_manager import PipelineStateManager
from sdc_engine_helpers.glue_jobs.manager import Manager


class MaintenanceManager(Manager):
    """
        Manage and maintain AWS Glue Pipeline jobs
    """
    date_utils = None
    glue = None
    pipeline_state_manager = None

    def __init__(self, **kwargs):
        self.service_for_update = True
        super().__init__(**kwargs)
        self.date_utils = DateUtils()
        self.glue = boto3.client('glue')
        self.pipeline_state_manager = PipelineStateManager()
        process = self.query_helper.get_process(slug='glue-jobs-maintenance')
        if process is not None:
            self.query_helper.process_id = process.id

    @decorators.retry_handler(SQLAlchemyError, total_tries=3, initial_wait=2)
    def perform_maintenance(self):
        """
            Execute Glue jobs when required

            Return:
                (bool) : the outcome of maintenance "updated", "not_updated", "blocked"
        """
        maintenance_outcome = "not_updated"

        # check if maintenance can be performed
        self.can_perform_maintenance = self.check_maintenance_is_allowed()

        if self.can_perform_maintenance:
            # Get all active client subscriptions for the supplied service
            for client in self.query_helper.get_clients():
                # Set up a flag to decide whether its necessary to update this subscription
                # after maintenance of this subscription
                update = False

                maintenance_mode, _ = self.query_helper.get_engine_entity(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=self.engine_slug,
                    entity_key='maintenance_mode',
                    from_cache=False
                )

                if maintenance_mode is None or maintenance_mode == 'off':
                    continue

                subscription = self.query_helper.get_subscription(
                    client_id=client.id,
                    service_id=self.service.id,
                    from_cache=False,
                    for_update=True
                )

                pipelines, engine_index = self.query_helper.get_engine_entity(
                    client_id=client.id,
                    service_id=self.service.id,
                    engine_slug=self.engine_slug,
                    entity_key='pipelines',
                    from_cache=False
                )

                if pipelines is not None:
                    response = self.perform_pipeline_maintenance(
                        client=client,
                        pipelines=pipelines,
                        maintenance_mode=maintenance_mode
                    )

                    if response.get('pipelines_executed') is True:
                        self.query_helper.update_pipelines(
                            subscription=subscription,
                            engine_index=engine_index,
                            value=response.get('pipelines')
                        )
                        update = True

                if update:
                    self.query_helper.update(model=subscription)
                    self.query_helper.flush_subscription_properties_cache(subscription=subscription)
                    maintenance_outcome = "updated"
        else:
            maintenance_outcome = "blocked"

        return maintenance_outcome

    def perform_pipeline_maintenance(
            self,
            *,
            client: Client,
            pipelines: list,
            maintenance_mode: str
    ) -> dict:
        """
            Perform the required maintenance on a list of pipelines

            args:
                client (Client): The client this maintenance is being performed for
                pipelines (list): A list of pipelines from the database to perform maintenance on
                maintenance_mode (str): The maintenance mode of the subscription
                                        (full/database_only)

            returns:
                result (dict): A dictionary with an updated flag and resultant solutions

        """
        # Set up a flag to return if the pipeline has executed
        pipelines_executed = False

        for index, pipeline in enumerate(pipelines):
            # The pipeline arn is required to continue maintenance for this pipeline
            job_name = pipeline.get('job_name', None)

            if job_name is None:
                continue

            state = self.pipeline_state_manager.get_state(
                pipeline=pipeline
            )

            if maintenance_mode == 'full' and state.get('should_execute') is True:
                print(
                    'Executing pipeline {job_name} for client: {client_name}'.format(
                        job_name=job_name,
                        client_name=client.name
                    )
                )

                arguments = {}

                parameters = pipeline.get('parameters', None)
                if parameters is not None:
                    for parameter in parameters:
                        key = '--{key}'.format(
                            key=parameter.get('key')
                        )
                        value = parameter.get(
                            'string_value',
                            json.dumps(
                                parameter.get(
                                    'json_value',
                                    {}
                                )
                            )
                        )

                        if key and value:
                            arguments[key] = str(value)

                response = self.glue.start_job_run(
                    JobName=job_name,
                    Arguments=arguments
                )

                job_run_id = response.get('JobRunId')
                print(
                    'Successfully started execution of {job_name} with run id {job_run_id}'.format(
                        job_name=job_name,
                        job_run_id=job_run_id
                    )
                )
                pipelines[index]['job_run_id'] = job_run_id

                pipelines[index]['last_executed_at'] = datetime.strftime(
                    datetime.now(),
                    self.date_utils.get_mysql_date_format()
                )

                next_execution_at = state.get('next_execution_at', None)
                if next_execution_at:
                    pipelines[index]['next_execution_at'] = next_execution_at

                pipelines_executed = True

        return {
            'pipelines_executed': pipelines_executed,
            'pipelines': pipelines
        }
