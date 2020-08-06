from odoo import api, fields, models


class Subject(models.Model):
    _name = 'subject'

    name = fields.Char()
    sequence = fields.Integer()
