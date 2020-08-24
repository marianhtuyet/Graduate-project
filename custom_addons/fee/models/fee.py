from datetime import date
from odoo import models, fields, api


class Fee(models.Model):
    _name = 'student.fee'

    student_id = fields.Many2one(
        'student.student',
        'pid',
        required=True
    )
    student_code = fields.Char(
        'Mã học sinh',
        related=student_id.student_code
    )
    class_id = fields.Char(
        'Lớp học',
        related=student_id.grade_id
    )
    date_study = fields.Integer('Số ngày')
    student_name = fields.Char(
        'Tên học sinh',
        related=student_id.student_name
    )
    date_absent = fields.Integer('Số ngày vắng')
    date_submit = fields.Datetime('Ngày nộp đến')
    date_to = fields.Datetime('Ngày đến')
    date_apply = fields.Datetime('Ngày áp dụng')
    month_submit = fields.Char('Tháng thu', compute='compute_month_submit')
    user_id = fields.Many2one(
        'res.users', "Người thu",
        default=lambda self: self.env.uid)
    line_ids = fields.One2many('fee.detail', 'fee_id')

    @api.depends('date_submit')
    def compute_month_submit(self):
        for rec in self:
            rec.month_submit = str(rec.date_submit.month) + ' / '+ str(rec.date_submit.year)

