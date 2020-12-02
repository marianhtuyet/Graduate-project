from odoo import api, fields, models


class MealFoodLine(models.Model):
    _name = 'meal.food.line'
    _description = 'Chi tiết món ăn'

    meal_food_id = fields.Many2one('meal.food', ondelete='cascade')
    nutrition_id = fields.Many2one('nutrition')
    menu_automatic_id = fields.Many2one('menu.automatic.weekly', ondelete='cascade')
    quantity = fields.Float('Lượng khẩu phần phù hợp với 1 trẻ', digits=(32,12), default=100)
    protein_a = fields.Float(
        'Đạm động vật',
        compute='_compute_balance_nutrition',
        store=True,
    )
    protein_v = fields.Float(
        'Đạm thực vật vật',
        compute='_compute_balance_nutrition',
        store=True,
    )
    lipit_a = fields.Float('Béo động vật', compute='_compute_balance_nutrition', store=True, )
    lipit_v = fields.Float('Béo thực vật', compute='_compute_balance_nutrition', store=True, )
    gluco = fields.Float('Đường', compute='_compute_balance_nutrition', store=True, )
    calo = fields.Float(compute='_compute_balance_nutrition', store=True, )

    @api.depends('nutrition_id', 'meal_food_id')
    def _compute_balance_nutrition(self):
        for rec in self:
            nutrition_id = rec.nutrition_id
            quantity = rec.quantity
            if nutrition_id:
                if nutrition_id.is_fruit:
                    rec.protein_v = nutrition_id.protein * quantity / 100
                    rec.lipit_v =  nutrition_id.lipit * quantity / 100
                elif rec.nutrition_id.is_animal:
                    rec.protein_a = nutrition_id.protein * quantity / 100
                    rec.lipit_a = nutrition_id.lipit * quantity / 100
                rec.gluco = nutrition_id.gluco * quantity / 100
                rec.calo = nutrition_id.calo * quantity / 100
        return True

