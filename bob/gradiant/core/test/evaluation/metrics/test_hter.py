#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np
from bob.gradiant.core import Hter

class UnitTestHter(unittest.TestCase):

	y_score = np.array((-1.2, -1.3, -0.25, 0.2, 0.6))
	y_true = np.array((1,2,2,0,0))
	expected_hter = 0.0

	def test_constructor_calls_sklearn_constructor(self):
		hter = Hter('HTER', threshold = 0.0)
		value, threshold = hter.compute(self.y_score, self.y_true)
		self.assertAlmostEquals(self.expected_hter,value)