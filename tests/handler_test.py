import pytest
import src.handler


def test_has_log_group_retention():
    log_group_description = {"retentionInDays": None}
    assert src.handler.has_log_group_retention(log_group_description) == False

    log_group_description = {"retentionInDays": 30}
    assert src.handler.has_log_group_retention(log_group_description) == True


def test_handle_request():
    handler = src.handler.LambdaHandler()
    handler_input = {}
