import unittest

import numpy as np

from fastestimator.op.numpyop.multivariate import Crop


class TestCrop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.height = 10
        cls.width = 10
        cls.single_input = [np.random.rand(28, 28, 3)]
        cls.single_output_shape = (10, 20, 3)
        cls.input_image_and_mask = [np.random.rand(28, 28, 3), np.random.rand(28, 28, 3)]
        cls.image_and_mask_output_shape = (10, 10, 3)

    def test_single_input(self):
        crop = Crop(x_min=0, y_min=10, x_max=20, y_max=20, image_in='x')
        output = crop.forward(data=self.single_input, state={})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output image shape'):
            self.assertEqual(output[0].shape, self.single_output_shape)

    def test_input_image_and_mask(self):
        crop = Crop(x_min=10, y_min=10, x_max=20, y_max=20, image_in='x', mask_in='x_mask')
        output = crop.forward(data=self.input_image_and_mask, state={})
        with self.subTest('Check output type'):
            self.assertEqual(type(output), list)
        with self.subTest('Check output image shape'):
            self.assertEqual(output[0].shape, self.image_and_mask_output_shape)
        with self.subTest('Check output mask shape'):
            self.assertEqual(output[1].shape, self.image_and_mask_output_shape)
