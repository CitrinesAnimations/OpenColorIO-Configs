#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines unit tests for the generated *ACES* configuration.
"""

import hashlib
import os
import re
import shutil
import tempfile
import unittest

from aces_ocio.util import files_walker
from aces_ocio.create_aces_config import (
    ACES_OCIO_CTL_DIRECTORY_ENVIRON,
    createACESConfig)

__author__ = ''
__copyright__ = ''
__license__ = ''
__maintainer__ = ''
__email__ = ''
__status__ = ''

__all__ = ['REFERENCE_CONFIG_ROOT_DIRECTORY',
           'HASH_TEST_PATTERNS',
           'UNHASHABLE_TEST_PATTERNS',
           'TestACESConfig']


# TODO: Investigate how the current config has been generated to use it for
# tests.
# REFERENCE_CONFIG_ROOT_DIRECTORY = os.path.abspath(
# os.path.join(os.path.dirname(__file__), '..', '..'))
REFERENCE_CONFIG_ROOT_DIRECTORY = '/colour-science/colour-ramblings/ocio/aces'

HASH_TEST_PATTERNS = ('\.3dl', '\.lut', '\.csp')
UNHASHABLE_TEST_PATTERNS = ('\.icc', '\.ocio')


class TestACESConfig(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        Initialises common tests attributes.
        """

        self.__aces_ocio_ctl_directory = os.environ.get(
            ACES_OCIO_CTL_DIRECTORY_ENVIRON, None)

        assert self.__aces_ocio_ctl_directory is not None, (
            'Undefined "{0}" environment variable!'.format(
                ACES_OCIO_CTL_DIRECTORY_ENVIRON))

        assert os.path.exists(self.__aces_ocio_ctl_directory) is True, (
            '"{0}" directory does not exists!'.format(
                self.__aces_ocio_ctl_directory))

        self.maxDiff = None
        self.__temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        """
        Post tests actions.
        """

        shutil.rmtree(self.__temporary_directory)

    @staticmethod
    def directory_hashes(directory, filters_in=None, filters_out=None):
        """
        """

        hashes = {}
        for path in files_walker(directory,
                                 filters_in=filters_in,
                                 filters_out=filters_out):
            with open(path) as file:
                hash = hashlib.md5(
                    re.sub('\s', '', file.read())).hexdigest()
            hashes[path.replace(directory, '')] = hash
        return hashes

    def test_ACES_config(self):
        """
        """

        self.assertTrue(createACESConfig(self.__aces_ocio_ctl_directory,
                                         self.__temporary_directory))

        reference_hashes = self.directory_hashes(
            REFERENCE_CONFIG_ROOT_DIRECTORY,
            HASH_TEST_PATTERNS)
        test_hashes = self.directory_hashes(
            self.__temporary_directory,
            HASH_TEST_PATTERNS)

        self.assertDictEqual(reference_hashes, test_hashes)

        # Checking that unashable files ('.icc', '.ocio') are generated.
        unashable = lambda x: (
            sorted([file.replace(x, '') for file in
                    files_walker(x, UNHASHABLE_TEST_PATTERNS)]))

        self.assertListEqual(unashable(REFERENCE_CONFIG_ROOT_DIRECTORY),
                             unashable(self.__temporary_directory))


if __name__ == '__main__':
    unittest.main()
