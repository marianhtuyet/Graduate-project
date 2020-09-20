from odoo import api, fields, models


class Subject(models.Model):
    _name = 'subject'

    name = fields.Char()
    name2 = fields.Char('English name')
    sequence = fields.Integer()
    units = fields.Integer()
    type_subject  = fields.Selection(
        [('1', 'Theology'),
         ('2', 'Philosophia')
         ], default='1'
    )
