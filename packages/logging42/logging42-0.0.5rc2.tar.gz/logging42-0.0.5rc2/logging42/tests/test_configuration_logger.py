"""
Tests for the configuration logger
"""
import pytest

from logging42.configuration_logger import ConfigurationRetriever


secrets = ("password", "pass", "secret", "token")


def keys() -> list:
    start = []
    middle = []
    end = []
    for s in secrets:
        start += [f"{s}safe", f"{s.upper()}safe"]
        middle += [f"safe{s}safe", f"safe{s.upper()}safe"]
        end += [f"safe{s}", f"safe{s.upper()}"]

    return start + middle + end


@pytest.fixture(scope="function")
def configuration_retriever():
    return ConfigurationRetriever(secrets=secrets)


@pytest.mark.parametrize("key", keys())
def test_censoring(configuration_retriever, key):
    configuration_retriever(key, "default")
    assert str(configuration_retriever) == f"{key}: <CENSORED>"


def test_safe(configuration_retriever):
    configuration_retriever("safe", "default")
    assert str(configuration_retriever) == f"safe: default"
