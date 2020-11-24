from odoo import api, fields, models


class MealFood(models.Model):
    _name = 'meal.food'
    _description = 'Món ăn'
    # _order = 'date_create'

    name = fields.Char('Name')
    is_breakfast = fields.Boolean('Bữa sáng')
    is_brunch = fields.Boolean('Phụ sáng')
    is_lunch = fields.Boolean('Tráng miệng')
    is_soup = fields.Boolean('Canh')
    is_main_lunch = fields.Boolean('Mặn')
    is_tea = fields.Boolean('Xế')
    is_tea2 = fields.Boolean('Xế 2')
    line_ids = fields.One2many('meal.food.line', 'meal_food_id')
