{
    'name': 'Nutrition',
    'summary': 'Management material in food',
    'description': """
Nutrition
============================

This module will manage and calculate nutrition in food
        """,
    'depends': [
        'report_xlsx', 'uom', 'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_food.xml',
        'views/nutrition.xml',
        'views/packaging.xml',
        'views/standard_material.xml',
        'views/supplier.xml',
        'views/type_food.xml',
        'menu/menu.xml',
    ],
    'installable': True,
    'application': True
}
