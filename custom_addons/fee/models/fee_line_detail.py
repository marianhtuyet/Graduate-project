from odoo import models, fields, api
from odoo.exceptions import UserError

class FeeLineDetail(models.Model):
    _name = 'fee.line.detail'

    fee_id = fields.Many2one('student.fee', 'Mã học phí')
    price_id =  fields.Many2one('fee.price', 'Mã đơn giá')
    fee_detail = fields.Many2one('fee.detail','Tên loại học phí')
    currency_id = fields.Many2one(
        'res.currency',
        default= lambda self: self.env.user.company_id.currency_id.id
    )
    amount = fields.Monetary(string='Số tiền', currency_field='currency_id')
    type_fee = fields.Selection([
        (1, 'Chi tiết học phí'),
        (2, 'Chi tiết đơn giá')
    ])

    @api.onchange('fee_detail')
    def onchange_fee_detail(self):
        for rec in self:
            rec.amount = rec.fee_detail.amount

    @api.depends('fee_id', 'price_id')
    def onchange_fee_price(self):
        for rec in self:
            if rec.fee_id and rec.price_id:
                raise UserError(_(
                    "Dòng chi tiết chỉ có thể là đơn giá hoặc chi tiết giá của học sinh."
                ))
