# coding: utf-8

import os
import fnmatch
import pkgutil
from token import NAME
from tokenize import generate_tokens

from django.test import TestCase
from django.conf import settings


PY_FILE_EXTENSION = '*.py'

NO_QUALITY_CHECK_LINE_MARK = '# noqa'
NO_QUALITY_CHECK_FILE_MARK = '# smelly_tokens: noqa'


class SmellyTokensTestCase(object):

    _tokens = []

    def test_check_token_exists(self):
        errors = []
        for module_name in getattr(settings, 'SMELLY_TOKENS_APPLICATIONS', []):
            module = pkgutil.get_loader(module_name).get_filename()
            module_dir = os.path.dirname(module)

            excludes = getattr(settings, 'SMELLY_TOKENS_EXCLUDE_DIRS', [])

            for file in self._get_py_files(module_dir, excludes):
                f = open(file)
                for kind, token, start, _, whole in \
                        generate_tokens(f.readline):
                    if whole.startswith(NO_QUALITY_CHECK_FILE_MARK):
                        break
                    if whole.strip().endswith(NO_QUALITY_CHECK_LINE_MARK):
                        continue
                    if kind != NAME:
                        continue
                    if token in self._tokens:
                        errors.append("'{}' left at '{}', line {}".format(
                            token, file, start[0]))
                f.close()

        self.assertTrue(len(errors) == 0, '\n'.join(errors))

    def _get_py_files(self, module_dir, exclude_dirs=[]):
        for directory, _, files in os.walk(module_dir):
            for file in fnmatch.filter(files, PY_FILE_EXTENSION):
                if [True for e in exclude_dirs if e in directory]:
                    continue
                yield os.path.join(directory, file)


class EvalTokenTestCase(SmellyTokensTestCase, TestCase):
    _tokens = ['eval']


class PdbTokenTestCase(SmellyTokensTestCase, TestCase):
    _tokens = ['pdb', 'ipdb']


class PrintTokenTestCase(SmellyTokensTestCase, TestCase):
    _tokens = ['print']
