from odoo import api, fields, models


class AmountModifyMenu(models.Model):
    _name = 'amount.modify.menu'
    _description = 'Điều chỉnh thực đơn sổ tính tiền ăn'

    standard_material_id = fields.Many2one('standard.material', 'Định mức dinh dưỡng')
    menu_food_id = fields.Many2one('menu.food', 'Tên thực đơn')
    is_breakfast = fields.Boolean('Thực đơn sáng')
    total_student = fields.Integer('Sĩ số')
    price = fields.Float('Giá 1 phần')
    payment_stock = fields.Float('Đã chi kho')
    payment = fields.Float('Đã chi cho')
    payment_service = fields.Float('Đã chi dịch vụ')
    exchange_payment = fields.Float('Chênh lệch cuối ngày')
    date_create = fields.Date('Ngày lập', default=fields.Date.today)
    line_ids = fields.One2many('amount.modify.menu.line', 'menu_food_id')
