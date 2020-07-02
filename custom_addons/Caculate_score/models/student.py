from odoo import _, api, fields, models


class Student(models.Model):
    _name = 'student'

    name = fields.Char()
    code = fields.Char('ID')
    date_of_birth = fields.Char()
    position_of_birth = fields.Char()
    congregation = fields.Char()


