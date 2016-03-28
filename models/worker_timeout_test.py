# coding=utf-8
# -*- coding: utf-8 -*-
import logging
import time
import datetime
import openerp.tools.config as config
from openerp import models, fields, api
from openerp.exceptions import UserError

_logger = logging.getLogger(__name__)

class WorkerTimeoutTest(models.Model):
    _name = 'worker_timeout_test'

    name = fields.Char()
    def _calc_limit_time_real(self):
        for record in self:
            record.limit_time_real = config['limit_time_real']
    limit_time_real = fields.Integer(name='limit-time-real',
                                     compute='_calc_limit_time_real',
                                     help="Value of the Odoo limit-time-real command line parameter.",
                                     readonly=True)


    def _calc_limit_time_real_cron(self):
        for record in self:
            record.limit_time_real_cron = config.get('limit_time_real_cron')
    limit_time_real_cron = fields.Integer(name='limit-time-real-cron',
                                          compute='_calc_limit_time_real_cron',
                                          help="Value of the Odoo limit-time-real-cron command "
                                               "line parameter.",
                                          readonly=True)
    worker_http_process_duration = fields.Integer(default=0,
                                                  help="Duration in second of "
                                                       "the process launched by "
                                                       "clicking on the button below")
    worker_cron_process_duration = fields.Integer(default=0,
                                                  help="Duration in second of the CRON Process")
    result = fields.Text()
    worker_result = fields.Text()


    @api.multi
    def launch_long_reponse_processing(self):
        """Wait the duration defined in self.worker_http_process_duration"""
        self.ensure_one()

        self.worker_http_result = ''
        self.env.cr.commit()

        if self.worker_http_process_duration < 0:
            self.worker_http_process_duration = 0

        time.sleep(self.worker_http_process_duration)
        msg = "===========> launch_long_response_processing() finished waiting for %ss at %s" % \
              (self.worker_http_process_duration, datetime.datetime.now(),)
        _logger.critical(msg)
        self.result = msg
        return

    def worker_long_processing(self, cr, uid, id, context=None):
        """A Job running for a long duration defined by self.worker_cron_process_duration
        :return:
        """
        _logger.critical("===========> worker_long_processing() started")
        start_time = datetime.datetime.now()
        wtt_id = self.search(cr, uid, [('id','=',id)])
        if not wtt_id:
            _logger.critical("===========> worker_long_processing() expects a valid 'worker_test_timeout_id' ! ")
            _logger.critical("===========> Enter something like (14,) in the job Arguments field. "
                             "Where 14 is the id of the worker_timeout_test to use.")
            _logger.critical("===========> Exiting without any processing !")
            return

        wtt_brw = self.browse(cr, uid, id)
        time.sleep(wtt_brw.worker_cron_process_duration)
        time.sleep(wtt_brw.worker_cron_process_duration)
        msg = "===========> worker_long_processing() started waiting at %s and finished waiting for %ss at %s" % \
              (start_time, wtt_brw.worker_cron_process_duration, datetime.datetime.now(),)
        _logger.critical(msg)
        wtt_brw.write({'worker_result': msg})
        return

