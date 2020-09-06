from odoo import api, fields, models


class Congregation(models.Model):
    _name = 'congregation'

    short_name = fields.Char()
    name = fields.Char()
    name2 = fields.Char('English name')

