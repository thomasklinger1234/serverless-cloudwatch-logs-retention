import os
import datetime
import logging
import boto3
import botocore.exceptions


def has_log_group_retention(log_group_description) -> bool:
    return log_group_description.get("retentionInDays") != None


class LoggingMixin(object):
    @property
    def logger(self):
        name = ".".join([self.__module__, self.__class__.__name__])
        return logging.getLogger(name)


class LambdaHandler(LoggingMixin):
    def __init__(self, session=None):
        super().__init__()
        self.session = session or boto3.Session()
        self.default_retention_in_days = 30
        self.default_log_group_prefix = "/"

    def handle_request(event, context):
        self.logger.info("received event [{}]".format(event))

        log_retention_in_days = event.get(
            "logRetentionInDays", self.default_retention_in_days
        )
        log_group_name_prefix = event.get(
            "logGroupNamePrefix", self.default_log_group_prefix
        )

        logs = self.session.client("logs")

        describe_log_groups_paginator = logs.get_paginator("describe_log_groups")
        describe_log_groups_input = {"logGroupNamePrefix": log_group_name_prefix}
        describe_log_groups_iterator = describe_log_groups_paginator.paginate(
            **describe_log_groups_input
        )

        for page in describe_log_groups_iterator:
            for log_group in page.get("logGroups", []):
                log_group_name = log_group["logGroupName"]

                if has_log_group_retention(log_group) == False:
                    put_retention_policy_input = {
                        "logGroupName": log_group_name,
                        "retentionInDays": log_retention_in_days,
                    }
                    try:
                        self.logger.info(
                            "updating retention policy for logGroup={log_group_name} to {policy}".format(
                                log_group_name=log_group_name,
                                policy=put_retention_policy_input,
                            )
                        )
                        logs.put_retention_policy(**put_retention_policy_input)
                    except botocore.exceptions.ClientError as e:
                        self.logger.warn(
                            "failed to put retention policy for logGroup={log_group_name}: {e}".format(
                                log_group_name=log_group_name, e=e
                            )
                        )


def handle_request(event, context):
    handler = LambdaHandler()
    handler_result = handler.handle_request(event, context)

    return handler_result
