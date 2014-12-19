# Ensure compatibility of Python 2 with Python 3 constructs
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import sambuca as sb
import pytest


class TestSambuca(object):

    """Sambuca test class"""

    def setup_class(cls):
        pass

    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_exception(self):
        '''Toy test for Sambuca Exceptions. Really just tests that they exist
        and are exported correctly
        '''
        with pytest.raises(sb.SambucaException) as ex:
            raise sb.SambucaException('pass')
        assert 'pass' in str(ex.value)