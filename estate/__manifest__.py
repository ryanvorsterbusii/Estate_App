# -*- coding: utf-8 -*-
{
    'name': "Real Estate App",

    'summary': """
        This is the estate module for developer How-Tos now on new ubuntu laptop""",

    'description': """
        This is a long description of module's purpose
    """,

    'author': "Ryan Vorster",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Estate App',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', "web"],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users.xml",
        "report/estate_reports.xml",
        "report/estate_report_views.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        "data/estate_demo.xml"
    ],
    'installable': True,
    'application': True,
    'autoinstall': False

}
