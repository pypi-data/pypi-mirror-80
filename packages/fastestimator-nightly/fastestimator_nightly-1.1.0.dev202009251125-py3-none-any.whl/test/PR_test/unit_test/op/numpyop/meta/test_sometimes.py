import unittest

import numpy as np

from fastestimator.op.numpyop.meta import Sometimes
from fastestimator.op.numpyop.univariate import Minmax


class TestSometimes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.single_input = [np.random.randint(16, size=(28, 28, 3))]
        cls.output_shape = (28, 28, 3)
        cls.multi_input = [np.random.randint(16, size=(28, 28, 3)), np.random.randint(16, size=(28, 28, 3))]

    def test_single_input(self):
        minmax = Minmax(inputs='x', outputs='x')
        sometimes = Sometimes(minmax, prob=0.75)
        output = sometimes.forward(data=self.single_input, state={})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output image shape'):
            self.assertEqual(output[0].shape, self.output_shape)

    def test_multi_input(self):
        minmax = Minmax(inputs=['x', 'y'], outputs=['x', 'y'])
        sometimes = Sometimes(minmax)
        output = sometimes.forward(data=self.multi_input, state={})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output list length'):
            self.assertEqual(len(output), 2)
        for img_output in output:
            with self.subTest('Check output image shape'):
                self.assertEqual(img_output.shape, self.output_shape)
