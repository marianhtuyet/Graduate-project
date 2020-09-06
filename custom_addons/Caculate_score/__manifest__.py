{
    'name': 'Calculate score',
    'summary': 'Add report to caculate score for student',
    'description': """
Calculate score
============================

This module will calculate the score of student and arrange score for student
        """,
    'depends': [
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/study_class.xml',
        'views/school_year.xml',
        'views/student.xml',
        'views/subject.xml',
        'views/congregation.xml',
        'menu/menu.xml',
        'report/student_score_report.xml',
    ],
    'installable': True,
}
