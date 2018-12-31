import pytest
import sys, os

def pytest_sessionstart(session):
    # Add microservice directory to path for test case imports to work
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))

def pytest_sessionfinish(session, exitstatus):
    # Cleanup, return sys.path to original state
    sys.path.append(os.path.realpath(os.path.dirname(__file__)))