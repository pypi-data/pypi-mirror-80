# confluent-kafka runtime environment variables

from os import environ
from nubium_utils import general_runtime_vars


def default_env_vars():
    """
    Environment variables that have defaults if not specified.
    """
    return {
        'POLL_TIMEOUT': environ.get('POLL_TIMEOUT', '10'),
        'TIMESTAMP_OFFSET_MINUTES': environ.get('TIMESTAMP_OFFSET_MINUTES', '0'),
        'RETRY_COUNT_MAX': environ.get('RETRY_COUNT_MAX', '0'),
        'PRODUCE_RETRY_TOPICS': environ.get('PRODUCE_RETRY_TOPICS', ''),
        'PRODUCE_FAILURE_TOPICS': environ.get('PRODUCE_FAILURE_TOPICS', '')}


def required_env_vars():
    """
    Environment variables that require a value (aka no default specified).
    """
    return {
        'CONSUME_TOPICS': environ['CONSUME_TOPICS']}


def all_env_vars():
    return {
        **general_runtime_vars.all_env_vars(),
        **default_env_vars(),
        **required_env_vars()
    }


env_vars = all_env_vars()