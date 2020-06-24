# -*- coding: utf-8 -*-
{
    'name': "personal Acciedent",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Personal',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','helpdesk_inherit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/personal_policy_report.xml',

        'data/mail_send.xml',

        # 'views/views.xml',
        'views/setup.xml',
        'views/personal_policy.xml',
        # 'views/benefits.xml',
        # 'views/excess.xml',
        'views/priceTable.xml',
        'views/menu_item.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}