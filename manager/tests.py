from django.test import TestCase
from django.core.urlresolvers import reverse
from subprocess import CalledProcessError

from .scripts.vagrant_boxes import _box_list, _global_status, _add_box, _remove_box, _init_env, _box_up, _box_destroy

import os
import tempfile
import unittest
import collections
import subprocess

Box = collections.namedtuple('Box', ['name', 'provider', 'version'])
Environment = collections.namedtuple('Environment', ['uid', 'name', 'provider', 'state', 'path'])

TEST_BOXNAME = 'local-jessie'
TEST_ADDBOX = ['local-jessie', '$HOME/gitdown/boxes/local-jessie-amd64.box']
TEST_URL = ['speedlight/jessie-vbguest']
TEST_BOX = Box(name='speedlight/jessie-vbguest', provider='virtualbox', version='8.3.0')
# TEST_BOX = Box(name='local-jessie', provider='virtualbox', version='0')
MIN_VBOX_VERSION = '5.0.14'
MIN_VAGRANT_VERSION = '1.8.1'

box_list = _box_list()
global_list = _global_status()


class VagrantBoxesScriptTests(TestCase):

    # @unittest.skip("not yet")
    def test_add_box(self):
        """
        Will download the box from TEST_URL.
        """
        self.assertEqual(_add_box(TEST_URL), 0)

    # @unittest.skip("not yet")
    def test_box_list_valid_output(self):
        """
        _box_list() should return a valid list,
        the name of the tuples should be 'Box',
        and must contain the info of test_box tuple
        """
        self.assertEqual(isinstance(box_list, list), True)
        self.assertEqual(type(box_list[0]).__name__, 'Box')
        self.assertEqual(TEST_BOX in box_list, True)

    @unittest.skip("not yet")
    def test_remove_box(self):
        """
        Should remove the box from Vagrant.
        """
        self.assertEqual(_remove_box(TEST_BOXNAME), 0)

    # @unittest.skip("not yet")
    def test_init_env(self):
        """
        _init_env should return exit code 0 (zero)
        the tmpdir is removed at finish.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            self.assertEqual(_init_env(TEST_BOXNAME, tmpdir), 0)

    # @unittest.skip("not yet")
    def test_box_up_destroy(self):
        """
        _box_up() should return confirmation of suscessful vagrant up command
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            _init_env(TEST_BOXNAME, tmpdir)
            self.assertEqual(_box_up(tmpdir), 0)
            self.assertEqual(_box_destroy(tmpdir), 0)

    # @unittest.skip("not yet")
    def test_global_status_valid_output(self):
        """
        _global_status() should return a valid list,
        the name of the tuples should be 'Environment',
        and must contain the info of the test_env tuple
        """
        self.assertEqual(isinstance(global_list, list), True)
        self.assertEqual(type(global_list[0]).__name__, 'Environment')

class ManagerIndexViewTest(TestCase):

    # @unittest.skip("not yet")
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

    # @unittest.skip("not yet")
    def test_index_view_box_list(self):
        """
        TEST_BOX info are shown in the view.
        """
        response = self.client.get(reverse('manager:index'))
        self.assertEqual(response.status_code, 200)

        test_boxes = response.context['all_boxes']
        self.assertEqual(TEST_BOX in test_boxes, True)

    # @unittest.skip("not yet")
    def test_index_view_global_status(self):
        """
        TEST_BOX info are shown in the view.
        """
        response = self.client.get(reverse('manager:index'))
        self.assertEqual(response.status_code, 200)

        test_boxes = response.context['all_envs']
        # self.assertEqual(TEST_BOX in test_boxes, True)

