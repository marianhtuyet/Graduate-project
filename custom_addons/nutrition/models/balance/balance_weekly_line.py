from odoo import api, fields, models
# models.TransientModel


class MenuAutomaticWeeklyLine(models.Model):
    _name = 'menu.automatic.weekly.line'

    menu_automatic_weekly_id = fields.Many2one('menu.automatic.weekly', ondelete='cascade')
    day_in_week = fields.Integer()
    breakfast1 = fields.Many2one(
        'meal.food',
        domain=[('is_breakfast', '=', True)]
    )
    breakfast2 = fields.Many2one(
        'meal.food',
        domain=[('is_brunch', '=', True)]
    )
    main_lunch = fields.Many2one(
        'meal.food',
        domain=[('is_main_lunch', '=', True)],
    )
    soup1 = fields.Many2one(
        'meal.food',
        domain=[('is_soup', '=', True)],
    )
    soup2 = fields.Many2one(
        'meal.food',
        domain=[('is_soup', '=', True)],
    )
    lunch = fields.Many2one(
        'meal.food',
        domain=[('is_lunch', '=', True)],
        help='Tráng miệng'
    )
    tea1 = fields.Many2one(
        'meal.food',
        domain=[('is_tea', '=', True)],
    )
    tea2 = fields.Many2one(
        'meal.food',
        domain=[('is_tea2', '=', True)],
    )

    @api.multi
    def calculate_menu_daily(self):
        for rec in self:
            meal_food_env = self.env['meal.food']
            breakfast1 = meal_food_env.search([('is_breakfast', '=', True)])
            breakfast2 = meal_food_env.search([('is_brunch', '=', True)])
            main_lunch = meal_food_env.search([('is_main_lunch', '=', True)])
            soup1 = meal_food_env.search([('is_soup', '=', True)])
            soup2 = meal_food_env.search([('is_soup', '=', True)])
            lunch = meal_food_env.search([('is_lunch', '=', True)])
            tea1 = meal_food_env.search([('is_tea', '=', True)])
            tea2 = meal_food_env.search([('is_tea2', '=', True)])

            last_index = breakfast1[-1]
            exams2_indexes = list(range(last_index + 1, last_index + 1 + len(exams2)))

            last_index = exams2_indexes[-1]
            exams3_indexes = list(range(last_index + 1, last_index + 1 + len(exams3)))

            last_index = exams3_indexes[-1]
            extra_exams_indexes = list(range(last_index + 1, last_index + 1 + len(extra_exams)))
