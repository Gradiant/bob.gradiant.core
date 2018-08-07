#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np
from bob.gradiant.core import Auc

class UnitTestAuc(unittest.TestCase):

	y_score = np.array((-0.50152192, -0.8802316 , -1.23112637,  1.33638315, -0.22550004, 2.01463408, -0.17242119,  2.29120825, -0.52607033, -2.03078131))
	y_true = np.array((1,0,0,0,0,0,1,1,1,0))
	expected_auc = 2.0/3.0
	def test_constructor_calls_sklearn_constructor(self):
		auc = Auc('AUC-1')

		value = auc.compute(self.y_score, self.y_true)

		self.assertAlmostEquals(self.expected_auc,value)