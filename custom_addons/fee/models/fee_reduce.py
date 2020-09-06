from datetime import date
from odoo import models, fields, api


class FeeReduce(models.Model):
    _name = 'fee.reduce'

    name = fields.Char('Tên')
    amount = fields.Float(string='Số phần trăm')
    status = fields.Selection(
        [(1, 'Đang sử dụng'),
         (0, 'Không sử dụng')
        ],
        default=1,
        string='Trạng thái'
    )
