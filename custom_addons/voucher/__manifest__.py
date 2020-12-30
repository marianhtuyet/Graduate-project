{
    'name': 'Voucher Breakfast',
    'summary': 'Management menu breakfast in the month',
    'description': """
Voucher Breakfast
============================

This module will summary voucher breakfast in the school in one month
        """,
    'depends': [
        'report_xlsx', 'uom', 'nutrition',
    ],
    'data': [
        'security/voucher_security.xml',
        'security/ir.model.access.csv',
        'report/voucher_breakfast.xml',
        'views/ingredient.xml',
        'views/voucher_breakfast.xml',
        'views/voucher_breakfast_line.xml',
        'menu/menu.xml',

    ],
    'installable': True,
    'application': True
}
