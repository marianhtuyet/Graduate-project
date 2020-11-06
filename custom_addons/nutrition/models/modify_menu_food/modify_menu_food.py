from odoo import api, fields, models


class ModifyMenuFood(models.Model):
    _name = 'modify.menu.food'
    _description = 'Điều chỉnh thực đơn'

    standard_material_id = fields.Many2one('standard.material', 'Định mức dinh dưỡng')
    menu_food_id = fields.Many2one('menu.food', 'Tên thực đơn')
    is_breakfast = fields.Boolean('Thực đơn sáng')
    name = fields.Char('Tên thực đơn 2')
    appetizer = fields.Char('Khai vị')
    breakfast = fields.Char('Món sáng')
    soup = fields.Char('Canh')
    soup2 = fields.Char('Canh 2')
    meat = fields.Char('Mặn')
    meat2 = fields.Char('Mặn 2')
    after_lunch = fields.Char('Ăn xế')
    after_lunch2 = fields.Char('Ăn xế 2')
    fruit = fields.Char('Phụ trưa xế')
    fruit2 = fields.Char('Phụ trưa xế 2')
    total_student = fields.Integer('Sĩ số')
    price = fields.Float('Giá 1 phần')
    date_create = fields.Date('Ngày lập', default=fields.Date.today)
    line_ids = fields.One2many('modify.menu.food.line', 'modify_menu_food_id')
    amount_line_ids = fields.One2many('amount.modify.menu.line', 'modify_menu_food_id')
