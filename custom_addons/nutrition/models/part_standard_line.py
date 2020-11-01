from odoo import api, fields, models


class PartStandardLine(models.Model):
    _name = 'part.standard.line'
    _description = 'Số phần chi tiết'

    part_standard_id = fields.Many2one('part.standard', 'Số phần định mức')
    nutrition_id = fields.Many2one('nutrition', 'Tên thực phẩm')
    quantity = fields.Float('Số lượng')
