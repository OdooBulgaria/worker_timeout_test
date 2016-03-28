# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Worker Timeout Test",

    'summary': "Allows to test worker timeout effect on long response page and job",

    'author': "Cyril MORISSE",
    'website': "http://twitter.com/cmorisse",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base'
    ],

    # always loaded
    'data': [
        'data/worker_timeout_test.xml',
        'data/ir_cron_worker.xml',
        'views/worker_timeout_test.xml',
    ],
    'application': False,
    'auto_install': False,
    'installable': True
}
