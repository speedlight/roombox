from django.test import TestCase
from django.core.urlresolvers import reverse
from subprocess import CalledProcessError

from .scripts.vagrant_boxes import _box_list, _global_status, _add_box, _init_env

import os
import tempfile
import unittest
import collections
import subprocess

Box = collections.namedtuple('Box', ['name', 'provider', 'version'])
Environment = collections.namedtuple('Environment', ['uid', 'name', 'provider', 'state', 'path'])

TEST_BOXNAME = 'speedlight/jessie-vbguest'
TEST_URL = ['speedlight/jessie-vbguest']
TEST_BOX = Box(name='speedlight/jessie-vbguest', provider='virtualbox', version='8.3.0')
MIN_VBOX_VERSION = '5.0.14'
MIN_VAGRANT_VERSION = '1.8.1'

box_list = _box_list()
global_list = _global_status()

class VagrantBoxesScriptTests(TestCase):

    @unittest.skip("not yet")
    def test_add_box(self):
        """
        Will download the box from TEST_URL.
        _add_box() should return exit code 0 (zero).
        """
        self.assertEqual(_add_box(TEST_BOX, 'force'), 0)

    def test_init_env(self):
        """
        _init_env should return exit code 0 (zero)
        the tmpdir is removed at finish.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(_init_env(TEST_BOXNAME, tmpdir), 0)
        # os.rmdir(tmpdir)

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

class ManagerIndexViewTest(TestCase):
    def test_index_view_versions(self):
        """
        Test that versions are shown,
        and minimal versions are met.
        """
        response = self.client.get(reverse('manager:index'))
        self.assertEqual(response.status_code, 200)

        min_versions = False
        versions = response.context['versions']
        vbox_version = versions['virtualbox_version']
        vagrant_version = versions['vagrant_version']
        if vbox_version >= MIN_VBOX_VERSION and vagrant_version >= MIN_VAGRANT_VERSION:
            min_versions = True
        self.assertEqual(min_versions, True)

    def test_index_view_box_list(self):
        """
        TEST_BOX info are shown in the view.
        """
        response = self.client.get(reverse('manager:index'))
        self.assertEqual(response.status_code, 200)

        test_boxes = response.context['all_boxes']
        self.assertEqual(TEST_BOX in test_boxes, True)

    def test_index_view_global_status(self):
        """
        TEST_BOX info are shown in the view.
        """
        response = self.client.get(reverse('manager:index'))
        self.assertEqual(response.status_code, 200)

        test_boxes = response.context['all_envs']
        # self.assertEqual(TEST_BOX in test_boxes, True)

