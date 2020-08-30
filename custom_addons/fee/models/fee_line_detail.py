from datetime import date
from odoo import models, fields, api


class FeeLineDetail(models.Model):
    _name = 'fee.line.detail'

    fee_id = fields.Many2one('student.fee', 'Mã học phí')
    fee_detail = fields.Many2one('fee.detail','Tên loại học phí')
    name = fields.Char('Tên')
    currency_id = fields.Many2one('res.currency', default= lambda self: self.sudo().company_id.currency_id)
    amount = fields.Monetary(string='Số tiền', currency_field='currency_id')

    @api.onchange('fee_detail')
    def onchange_fee_detail(self):
        for rec in self:
            rec.name = rec.fee_detail.name
            rec.amount = rec.fee_detail.amount
