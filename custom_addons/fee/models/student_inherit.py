from datetime import date
from odoo import models, fields, api


class StudentStudent(models.Model):
    _inherit = 'student.student'

    reduce_code = fields.Many2one('fee.reduce', 'Mã miễn giảm')
