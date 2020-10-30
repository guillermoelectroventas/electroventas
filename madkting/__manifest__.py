# -*- coding: utf-8 -*-
{
    'name': "Yuju",

    'summary': """
        Integration with Yuju's platform""",

    'description': """
        Module integration with Yuju's software platform.
        - Create orders into your odoo software from marketplaces like Mercado Libre, Amazon, etc..
        - Create products from Yuju platform into odoo
        - Update your stock from odoo to your Yuju account.
    """,

    'author': "Israel Calderón Aguilar",
    'website': "https://yuju.io/",
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'stock',
        'component_event'
    ],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}