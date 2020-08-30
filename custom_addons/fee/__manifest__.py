{
    'name': 'Student fee',
    'summary': 'Add module to check fee of student',
    'description': """
Student fee
============================

This module will save, edit, create new record about fee of student
        """,
    'depends':['school'],
    'data': [
        'security/ir.model.access.csv',
        'views/fee_view.xml',
        'views/fee_detail_view.xml',
        'menu/menu.xml',
    ],
    'installable': True,
}
