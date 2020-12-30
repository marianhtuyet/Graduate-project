from odoo import api, fields, models


class AmountModifyMenuLine(models.Model):
    _name = 'amount.modify.menu.line'

    amount_modify_menu_id = fields.Many2one('amount.modify.menu')
    modify_menu_food_id = fields.Many2one('modify.menu.food', 'Tên DCTD thực đơn')
    nutrition_id = fields.Many2one('nutrition', 'Thực phẩm')
    price = fields.Float('Đơn giá')
    quantity = fields.Float('Số lượng')
    is_stock = fields.Boolean('Kho')
