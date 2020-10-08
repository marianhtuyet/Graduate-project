from odoo import _, api, models, fields
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
    count_date = fields.Integer(string='Số ngày', default=0)
    price = fields.Monetary(string='Đơn giá', currency_field='currency_id', related='fee_detail.amount')
    amount = fields.Monetary(string='Tổng cộng', currency_field='currency_id')
    type_fee = fields.Selection([
        (1, 'Chi tiết học phí'),
        (2, 'Chi tiết đơn giá')
    ])

    @api.onchange('fee_detail')
    def onchange_fee_detail(self):
        for rec in self:
            detail = rec.fee_detail
            rec.price = detail.amount
            rec.amount = detail.amount if detail.type_fee != 1 else rec.count_date * detail.amount


    @api.depends('fee_id', 'price_id')
    def onchange_fee_price(self):
        for rec in self:
            if rec.fee_id:
                rec.count_date = rec.fee_id.date_study - rec.fee_id.date_absent
            if rec.fee_id and rec.price_id:
                raise UserError(_(
                    "Dòng chi tiết chỉ có thể là đơn giá hoặc chi tiết giá của học sinh."
                ))
