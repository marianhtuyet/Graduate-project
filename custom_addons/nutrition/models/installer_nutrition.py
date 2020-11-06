import logging

from odoo import api, models

logger = logging.getLogger("installer.kfa.all")


class InstallerNutrition(models.TransientModel):
    _name = "nutrition.installer"
    _inherit = "installer.helper"

    @api.model
    def start(self):
        self.run_only_once(
            "nutrition.installer",
            [
                "update_name_nutrition",
            ],

        )
        self.recompute_balance_nutrition()
        return True

    @api.multi
    def update_name_nutrition(self):
        nutrition = self.env["nutrition"]
        nutritions = nutrition.search([])
        for rec in nutritions:
            rec.name = rec.name2
        return True

    @api.model
    def recompute_balance_nutrition(self):
        menu_env = self.env["modify.menu.food.line"]
        menus = menu_env.search([])
        self.env.add_todo(menu_env._fields["protein_a"], menus)
        self.env.add_todo(menu_env._fields["protein_v"], menus)
        self.env.add_todo(menu_env._fields["qty_g"], menus)
        self.env.add_todo(menu_env._fields["lipit_a"], menus)
        self.env.add_todo(menu_env._fields["lipit_v"], menus)
        self.env.add_todo(menu_env._fields["gluco"], menus)
        self.env.add_todo(menu_env._fields["calo"], menus)
        self.env.add_todo(menu_env._fields["amount"], menus)
        self.env.add_todo(menu_env._fields["qty_eat"], menus)
        self.env.add_todo(menu_env._fields["constant"], menus)
        self.env.add_todo(menu_env._fields["qty_buy"], menus)
        self.env.add_todo(menu_env._fields["qty_uom"], menus)
        menu_env.recompute()
        return True

