from odoo import api, fields, models


class VoucherBreakfast(models.Model):
    _name = 'voucher.breakfast'

    company_id = fields.Many2one(
        'res.company',
        'Đơn vị', default=lambda self: self.env.user.company_id.id)
    name = fields.Char('Họ tên người nhận hàng')
    sequence = fields.Char('Số ')
    street = fields.Char('Địa chỉ', related='company_id.street')
    total_student = fields.Integer('Số trẻ')
    receiver = fields.Char('Người nhận', default = lambda self: self.env.user.name)
    name_food = fields.Char('Điểm tâm', help="Món ăn")
    transfer_user  = fields.Char("Người giao")
    create_user = fields.Char("Người tạo phiếu")
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.user.company_id.currency_id.id
    )
    total_amount = fields.Monetary(
        'Tổng cộng',
        compute='_compute_total_amount',
        currency_field = 'currency_id'
    )
    total_2_text = fields.Char('Bằng chữ')
    line_ids = fields.One2many('voucher.breakfast.line', 'voucher_id')

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(line.amount for line in rec.line_ids)
