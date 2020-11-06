from odoo import api, fields, models


class StandardMaterial(models.Model):
    _name = 'standard.material'
    _description = 'Định mức dinh dưỡng'

    name = fields.Char('Tên định mức')
    name2 = fields.Char('Tên định mức 2')
    protein_a = fields.Float('Đạm động vật')
    protein_v = fields.Float('Đạm thực vật')
    lipit_a = fields.Float('Béo động vật')
    lipit_v = fields.Float('Béo thực vật')
    gluco = fields.Float('Đường')
    calo = fields.Float('Calo')
    rate_min = fields.Float('Tỷ lệ đạt thấp nhất')
    rate_max = fields.Float('Tỷ lệ đạt cao nhất')
