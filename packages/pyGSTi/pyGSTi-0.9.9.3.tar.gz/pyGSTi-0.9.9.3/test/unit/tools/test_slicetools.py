from ..util import BaseCase
import numpy as np

from pygsti.tools.slicetools import *

N = 100
slices = []
for i in range(1, N):
    for j in range(1, N):
        for k in [1, 2]:
            slices.append(slice(i, j, k))


class SliceToolsTester(BaseCase):
    def test_length(self):
        for s in slices:
            length(s)
        self.assertEqual(length(slice(10)), 0)
        self.assertEqual(length(slice(1, 10)), 9)

    def test_indices(self):
        for s in slices:
            indices(s)
        indices(slice(10))
        # TODO assert correctness

    def test_intersect(self):
        intersect(slice(None, 10, 1), slice(1, 10, 1))
        intersect(slice(1, 10, 1), slice(None, 10, 1))
        intersect(slice(1, None, 1), slice(1, 10, 1))
        intersect(slice(1, 10, 1), slice(1, None, 1))
        intersect(slice(10, -10, 1), slice(10, -10, 1))
        # TODO assert correctness

    def test_list_to_slice(self):
        self.assertEqual(list_to_slice([]), slice(0, 0))
        self.assertEqual(list_to_slice([1, 2, 3, 4]), slice(1, 5))
        self.assertEqual(list_to_slice(slice(0, 4)), slice(0, 4))
        with self.assertRaises(ValueError):
            list_to_slice([0, 1, 2, 3, 10])  # doesn't correspond to a slice

    def test_asarray(self):
        self.assertArraysAlmostEqual(as_array(slice(0, 10)), np.arange(10))
        self.assertArraysAlmostEqual(as_array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), np.arange(10))
