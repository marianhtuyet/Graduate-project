from odoo import api, fields, models


class Packaging(models.Model):
    _name = 'packaging'

    name = fields.Char()
