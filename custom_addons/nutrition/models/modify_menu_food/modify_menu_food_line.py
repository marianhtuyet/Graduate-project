from odoo import api, fields, models


class ModifyMenuFoodLine(models.Model):
    _name = 'modify.menu.food.line'
    _description = 'Chi tiết điều chỉnh thực đơn'

    modify_menu_food_id = fields.Many2one('modify.menu.food')
    nutrition_id = fields.Many2one('nutrition')
    quantity = fields.Float('Lượng khẩu phần đơn vị tính')
    price = fields.Float('Đơn giá')
