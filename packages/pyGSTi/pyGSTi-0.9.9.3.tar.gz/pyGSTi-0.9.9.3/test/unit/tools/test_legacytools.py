from ..util import BaseCase

from pygsti.tools import legacytools


class LegacyTestCase(BaseCase):
    def test_deprecation_warning(self):

        @legacytools.deprecated_fn("Replacement function name")
        def oldFn(x):
            return x

        oldFn(5)
        # TODO assert correctness
