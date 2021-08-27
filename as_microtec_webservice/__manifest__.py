# -*- coding: utf-8 -*-
{
    'name' : "TIAMERICA MICROTEC Webservices",
    'version' : "1.1.3",
    'author'  : "TIAMERICA",
    'description': """
Webservice Microtec
    """,
    'category' : "Sale",
    'depends' : [
        "base",
        "purchase",
        "stock",
        "sale_management",
        ],
    'website': 'http://www.ahorasoft.com',
    'data' : [
        'security/ir.model.access.csv',
        'views/as_tienda.xml',
        'views/as_stock_warehouse.xml',
             ],
    'demo' : [],
    'installable': True,
    'auto_install': False
}
