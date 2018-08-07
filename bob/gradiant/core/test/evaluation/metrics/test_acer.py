#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np
from bob.gradiant.core import Acer

class UnitTestAuc(unittest.TestCase):

	y_score = np.array((0.0, 0.2, 0.2, 0.5, 0.6))
	y_true = np.array((1,2,2,0,0))
	expected_acer = 0.0
	def test_constructor_calls_sklearn_constructor(self):
		acer = Acer('ACER', threshold = 0.25)

		value, threshold = acer.compute(self.y_score, self.y_true)

		self.assertAlmostEquals(self.expected_acer,value)