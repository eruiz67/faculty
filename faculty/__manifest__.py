# -*- coding: utf-8 -*-
{
    'name': "faculty",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ernesto Ruiz",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/user_views.xml',
        'views/course_views.xml',
        'views/professor_views.xml',
        'views/exam_views.xml',
        'wizards/program_course_wizard.xml',
        'wizards/response_exam_wizard.xml',
        'wizards/qualify_exam_wizard.xml',
        'wizards/course_global_score_wizard.xml',
        'wizards/enroll_wizard.xml',
        'views/actions.xml',
        'views/menus.xml',
        'data/cron.xml',
        'views/templates.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':
    True
}