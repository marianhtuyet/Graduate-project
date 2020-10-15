from odoo import _, api, models, fields
from odoo.exceptions import UserError

class VoucherBreakfastline(models.Model):
    _name = 'voucher.breakfast.line'

    voucher_id =  fields.Many2one('voucher.breakfast', 'Mã phiếu sáng')
    currency_id = fields.Many2one(
        'res.currency',
        default= lambda self: self.env.user.company_id.currency_id.id
    )
    quantity = fields.Float('Số lượng')
    price = fields.Monetary(string='Đơn giá', currency_field='currency_id')
    amount = fields.Monetary(string='Thành tiền', currency_field='currency_id', compute='_compute_amount')
    ingredient_id = fields.Many2one('ingredient', 'Tên loại thực phẩm')
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        related='ingredient_id.uom_id',
        readonly=False
    )

    @api.depends('price', 'quantity')
    def _compute_amount(self):
        for rec in self:
            print("*"*80)
            print('rec.quantity:  ', rec.quantity)
            print('rec.price: ', rec.price)
            rec.amount = rec.quantity * rec.price

    @api.onchange('price', 'quantity')
    def onchange_quantity(self):
        for rec in self:
            print("1"*80)
            rec.amount = rec.quantity * rec.price
