#!/bin/env python
# -*-coding:utf-8 -*
"""
Test of the config.py module.
"""
# pylint: disable=missing-function-docstring
# No need to add a docstring to each tests.

import os.path
import unittest
from context import model


class ConfigTest(unittest.TestCase):
    """
    This class will test the Config class.
    """

    def setUp(self):
        self.path1 = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  "data/config.json"))
        os.makedirs(os.path.dirname(self.path1), exist_ok=True)
        with open(self.path1, "w") as filep:
            filep.write(
                "{\"archive\":{\"input\": [\"data/config.json\",\
\"data/test\"], \"output\": \"data/tar\"}}")
        self.path2 = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  "data/config2.json"))
        with open(self.path2, "w") as filep:
            filep.write(
                "{\"former\": [\"data/config.json\",\
\"data/test\"], \"output\": \"data/tar\"}")

    def test_item_search_archive(self):
        json_config = model.ConfigManager(self.path1)
        result = json_config.item_search(("archive",))
        self.assertEqual(result, {'input': ['data/config.json',
                                            'data/test'],
                                  'output': 'data/tar'})

    def test_item_search_input(self):
        json_config = model.ConfigManager(self.path1)
        result = json_config.item_search(("archive", "input"))
        self.assertEqual(result, ['data/config.json',
                                  'data/test'])

    def test_item_search_output(self):
        json_config = model.ConfigManager(self.path1)
        result = json_config.item_search(("archive", "output"))
        self.assertEqual(result, 'data/tar')

    def test_item_search_archive_not_exist(self):
        json_config = model.ConfigManager(self.path2)
        result = json_config.item_search(("archive",))
        self.assertEqual(result, None)

    def test_item_search_input_not_exist(self):
        json_config = model.ConfigManager(self.path2)
        result = json_config.item_search(("archive", "input"))
        self.assertEqual(result, None)

    def tearDown(self):
        os.remove(self.path1)
        os.remove(self.path2)


class DirHandlerTest(unittest.TestCase):
    """
    This class will test the DirHandler class.
    """
    def setUp(self):
        self.path1 = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  "test1"))
        self.path2 = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                  "test2"))
        os.mkdir(self.path2)

    def test_connect(self):
        directory = model.DirHandler(self.path1)
        directory.connect()
        self.assertEqual(os.access(self.path1, os.F_OK), True)

    def test_is_writable(self):
        directory = model.DirHandler(self.path2)
        self.assertEqual(directory.is_writable(), True)

    def tearDown(self):
        try:
            os.rmdir(self.path1)
        except FileNotFoundError:
            pass
        try:
            os.rmdir(self.path2)
        except FileNotFoundError:
            pass


def suite_config_test():
    """
    List of tests to run to test Config class.
    """
    tests = ['test_item_search_archive',
             'test_item_search_input',
             'test_item_search_output',
             'test_item_search_archive_not_exist',
             'test_item_search_input_not_exist']
    return unittest.TestSuite(map(ConfigTest, tests))


def suite_dirhandler_test():
    """
    List of tests to run to test DirHandler class.
    """
    tests = ['test_connect',
             'test_is_writable']
    return unittest.TestSuite(map(DirHandlerTest, tests))


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite_config_test())
    unittest.TextTestRunner(verbosity=2).run(suite_dirhandler_test())
