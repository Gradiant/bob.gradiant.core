#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.evaluation.metrics.acer import Acer
from bob.gradiant.core.classes.evaluation.metrics.apcer import Apcer
from bob.gradiant.core.classes.evaluation.metrics.bpcer import Bpcer
from bob.gradiant.core.classes.evaluation.metrics.eer import Eer
from bob.gradiant.core.classes.evaluation.metrics.far import Far
from bob.gradiant.core.classes.evaluation.metrics.hter import Hter
from bob.gradiant.core.classes.evaluation.metrics.auc import Auc

metric_provider = {'EER': Eer('EER'),
                   'ACER': Acer('ACER'),
                   'APCER': Apcer('APCER'),
                   'BPCER': Bpcer('BPCER'),
                   'AUC': Auc('AUC'),
                   'FAR01': Far('Far', far_value=0.1),
                   'FAR05': Far('Far', far_value=0.5),
                   'FAR1': Far('Far', far_value=1.0),
                   'FAR5': Far('Far', far_value=5.0),
                   'HTER': Hter('HTER')
                   }
