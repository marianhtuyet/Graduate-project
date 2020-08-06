
from datetime import datetime
from odoo import api, fields, models


class StudentClassWizard(models.TransientModel):
    _name = 'student.class.wizard'
    _description = 'student.class.wizard'


    report_date = fields.Date(required=True, default=datetime.now())
    user_create = fields.Char(required=True)

    @api.multi
    def print_xlsx_report(self):
        self.ensure_one()
        return self.env.ref('caculate_score.student_score_report.xml'
                            ).report_action(self)

