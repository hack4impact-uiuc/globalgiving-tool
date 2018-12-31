import pytest
import sys, os

"""
Contains methods used before pytest collects all the tests within the microservices directory. Adds the correct directory such that
all of the test imports in each microservice will be found and the test cases will run.
"""


def pytest_sessionstart(session):
    # Add microservice directory to path for test case imports to work
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))


def pytest_sessionfinish(session, exitstatus):
    # Cleanup, return sys.path to original state
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))
