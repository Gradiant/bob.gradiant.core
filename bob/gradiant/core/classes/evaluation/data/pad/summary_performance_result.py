#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
class SummaryPerformanceResult(object):

   def __init__(self, name_database, name_algorithm, configuration, threshold_dev, eer_dev, hter, acer, apcer, bpcer):
       self.name_database = name_database
       self.name_algorithm = name_algorithm
       self.configuration = configuration
       self.threshold_dev = threshold_dev
       self.eer_dev = eer_dev
       self.hter = hter
       self.acer = acer
       self.apcer = apcer
       self.bpcer = bpcer

   @staticmethod
   def get_headers():
       return ['System',
               'Configuration',
               'Threshold@Dev',
               'EER@Dev',
               'HTER@EER',
               'ACER@EER',
               'APCER@EER',
               'BPCER@EER']

   def __str__(self):
        return 'SummaryPerformanceResult : \n\t {} | {} \n\t {} \n\t {} \n\t {} \n\t {}'.format(self.name_algorithm,
                                                                   self.configuration,
                                                                   'EER@Dev : ' + str(self.threshold_dev),
                                                                   'Threshold@Dev : ' + str(self.eer_dev),
                                                                   'HTER@EER : '+ str(self.hter),
                                                                   'ACER@EER : ' + str(self.acer),
                                                                   'APCER@EER : ' + str(self.apcer),
                                                                   'BPCER@EER : ' + str(self.bpcer))

   def get_performance_row(self):
       return [self.name_algorithm,
               self.configuration,
               str('%.2f%%' % (self.threshold_dev)),
               str('%.2f%%' % (self.eer_dev)),
               str('%.2f%%' % (self.hter)),
               str('%.2f%%' % (self.acer)),
               str('%.2f%%' % (self.apcer)),
               str('%.2f%%' % (self.bpcer))]


