from datetime import date
from odoo import models, fields, api


class FeeDetail(models.Model):
    _name = 'fee.detail'

    name = fields.Char('Tên')
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.user.company_id.currency_id.id
    )
    amount = fields.Monetary(string='Số tiền', currency_field='currency_id')
    type_fee = fields.Selection(
        [(1, 'Tính theo ngày'),
         (2, 'Tính theo tháng'),
         (3, 'Năng khiếu'),
        ],
        default=2,
        string='Loại tiền'
    )
    status = fields.Selection(
        [(1, 'Đang sử dụng'),
         (0, 'Không sử dụng')
        ],
        default=1,
        string='Trạng thái'
    )
