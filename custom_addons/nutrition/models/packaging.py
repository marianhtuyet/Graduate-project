from odoo import api, fields, models


class Packaging(models.Model):
    _name = 'packaging'
    _description = 'Bao bì'

    name = fields.Char()
