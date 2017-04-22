"""Common helper functions for tests."""
import os


def load_fixture(filename):
    """Load a fixture from a file."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(path) as fptr:
        return fptr.read()
