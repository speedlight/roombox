from django.test import TestCase
from subprocess import CalledProcessError

from .scripts.vagrant_boxes import _box_list, _global_status, _add_box

import unittest
import collections
import subprocess

Box = collections.namedtuple('Box', ['name', 'provider', 'version'])
Environment = collections.namedtuple('Environment', ['uid', 'name', 'provider', 'state', 'path'])

TEST_URL = ['speedlight/jessie-vbguest']
TEST_BOX = Box(name='speedlight/jessie-vbguest', provider='virtualbox', version='8.3.0')

box_list = _box_list()
global_list = _global_status()

class CheckOutputVagrantCommands(TestCase):

    @unittest.skip("not yet")
    def test_add_box(self):
        """
        Will download the box from TEST_URL.
        _add_box() should return exit code 0 (zero).
        """
        self.assertEqual(_add_box(TEST_BOX, 'force'), 0)

    def test_box_list_valid_output(self):
        """
        _box_list() should return a valid list,
        the name of the tuples should be 'Box',
        and must contain the info of test_box tuple
        """
        self.assertEqual(isinstance(box_list, list), True)
        self.assertEqual(type(box_list[0]).__name__, 'Box')
        self.assertEqual(TEST_BOX in box_list, True)

    def test_global_status_valid_output(self):
        """
        _global_status() should return a valid list,
        the name of the tuples should be 'Environment',
        and must contain the info of the test_env tuple
        """
        self.assertEqual(isinstance(global_list, list), True)
        self.assertEqual(type(global_list[0]).__name__, 'Environment')

