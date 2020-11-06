from odoo import api, fields, models


class TypeFood(models.Model):
    _name = 'type.food'

    name = fields.Char('Mã')
    name2 = fields.Char('Tên')
    group_name = fields.Char()
