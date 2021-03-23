import os

TESTS_SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'samples')


def open_test_file(filename):
    return open(os.path.join(TESTS_SAMPLES_DIR, filename), 'r')