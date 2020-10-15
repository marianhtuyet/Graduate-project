from odoo import api, fields, models


class Ingredient(models.Model):
    _name = 'ingredient'

    name = fields.Char()
    name2 = fields.Char('English name')
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure')