from datetime import date
from odoo import models, fields, api


class FeeDetail(models.Model):
    _name = 'fee.detail'

    fee_id = fields.Many2one('student.fee', 'Mã học phí')
    name = fields.Char('Tên')
    currency_id = fields.Many2one('res.currency', default= lambda self: self.sudo().company_id.currency_id)
    amount = fields.Monetary(string='Số tiền', currency_field='currency_id')
    status = fields.Selection(
        [('1', 'Đang sử dụng'),
         ('0', 'Không sử dụng')
        ],
        string='Trạng thái'
    )
