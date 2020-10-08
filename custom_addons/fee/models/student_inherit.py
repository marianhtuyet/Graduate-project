from datetime import date
from odoo import models, fields, api


class StudentStudent(models.Model):
    _inherit = 'student.student'

    reduce_code = fields.Many2one('fee.reduce', 'Mã miễn giảm')
    customize_code = fields.Char('Mã học sinh')
    custom_name = fields.Char('Tên học sinh')
    father_name = fields.Char('Tên Cha')
    father_job = fields.Char('Nghề nghiệp Cha')
    mother_name = fields.Char('Tên Mẹ')
    mother_job = fields.Char('Nghề nghiệp Mẹ')
    phone_father = fields.Char('SĐT Cha')
    phone_mother = fields.Char('SĐT Mẹ')

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = '{} - {}'.format(rec.customize_code, rec.custom_name)
            result.append((rec.id, name))
        return result
