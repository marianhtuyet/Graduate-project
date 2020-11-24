{
    'name': 'Nutrition',
    'summary': 'Management material in food',
    'description': """
Nutrition
============================

This module will manage and calculate nutrition in food
        """,
    'depends': [
        'report_xlsx', 'uom', 'product', 'Caculate_score'
    ],
    'data': [

        'security/ir.model.access.csv',
        'views/amount_modify_menu/amount_modify_menu.xml',
        'views/amount_modify_menu/amount_modify_menu_line.xml',
        'views/menu_food/menu_food.xml',
        'views/menu_food/menu_food_line.xml',
        'views/meal_food/meal_food.xml',
        'views/meal_food/meal_food_line.xml',
        'views/nutrition.xml',
        'views/packaging.xml',
        'views/part_standard.xml',
        'views/part_standard_line.xml',
        'views/standard_material.xml',
        'views/supplier.xml',
        'views/type_food.xml',
        'views/modify_menu_food/modify_menu_food.xml',
        'views/modify_menu_food/modify_menu_food_line.xml',
        'views/balance/balance_weekly.xml',
        'views/balance/balance_weekly_line.xml',
        'menu/menu.xml',
        'data/installer_helper.xml',
        'data/installer_nutrition.xml',
        'data/ir_cron_data.xml',
        'report/nutrition_balance_xlsx.xml',

        'wizard/balance_weekly_wizard.xml',
    ],
    'installable': True,
    'application': True
}
