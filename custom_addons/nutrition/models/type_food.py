from odoo import api, fields, models


class TypeFood(models.Model):
    _name = 'type.food'

    name = fields.Char()
    group_name = fields.Char()
