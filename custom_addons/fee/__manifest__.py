{
    'name': 'Student fee',
    'summary': 'Add module to check fee of student',
    'description': """
Student fee
============================

This module will save, edit, create new record about fee of student
        """,
    'depends':['school', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_fee.xml',
        'report/report_fee_notify.xml',
        'report/report_fee_receipt.xml',
        'report/report_fee_invitation.xml',
        'views/fee_view.xml',
        'views/fee_detail_view.xml',
        'views/fee_line_detail_view.xml',
        'views/fee_reduce_view.xml',
        'views/fee_price_view.xml',
        'views/student_view_inherit.xml',
        'menu/menu.xml',
    ],
    'installable': True,
    'application': True
}
