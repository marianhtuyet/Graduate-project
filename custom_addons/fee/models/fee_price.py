from odoo import models, fields, api


class FeePrice(models.Model):
    _name = 'fee.price'

    name = fields.Char('Tên')
    amount = fields.Float(string='Số phần trăm')
    status = fields.Selection(
        [(1, 'Đang sử dụng'),
         (0, 'Không sử dụng')
        ],
        default=1,
        string='Trạng thái'
    )
    date_apply = fields.Date('Ngày áp dụng')
    detail_line_ids = fields.One2many('fee.line.detail', 'price_id')

    @api.multi
    def add_all_fee(self):
        fee_detail_env = self.env['fee.detail']
        fee_line_detail = self.env['fee.line.detail']
        for rec in self:
            list_fee_detail = fee_detail_env.search([('status', '=', 1)])
            for fee_detail in list_fee_detail:
                detail = fee_line_detail.create({
                    'price_id': rec.id,
                    'fee_detail': fee_detail.id,
                    'amount': fee_detail.amount,
                    'currency_id': fee_detail.currency_id.id,
                    'type_fee': 2
                })
        return True
