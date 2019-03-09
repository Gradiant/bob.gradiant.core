#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np
from bob.gradiant.core import Iapmr

class UnitTestIapmr(unittest.TestCase):

	y_score = np.array((0.77, 0.3, 0.2, 0.8, 0.95))
	y_true = np.array((1,2,2,0,0))
	expected_iapmr = {}
	expected_iapmr[1] = 1.0
	expected_iapmr[2] = 0.0
	def test_constructor_calls_sklearn_constructor(self):
		iapmr = Iapmr('IAPMR', threshold = 0.75)

		value, threshold = iapmr.compute(self.y_score, self.y_true)

		self.assertDictEqual(self.expected_iapmr,value)