from odoo import api, fields, models


class PartStandard(models.Model):
    _name = 'part.standard'
    _description = 'Số phần định mức'

    type_part = fields.Char('Loại số phần')
    standard_material_id = fields.Many2one('standard.material', 'Định mức dinh dưỡng')
    part_min = fields.Float('Số phần tối thiểu')
    part_max = fields.Float('Số phần tối đa')
    line_ids = fields.One2many('part.standard.line', 'part_standard_id')
