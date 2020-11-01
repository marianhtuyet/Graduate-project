from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    id_code = fields.Char('Mã nhà cung cấp')
    deliver = fields.Char('Người giao hàng')
    shopkeeper = fields.Char('Chủ cửa hàng')
