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
        self.update_name_nutrition()
        return True

    @api.multi
    def update_name_nutrition(self):
        nutrition = self.env["nutrition"]
        nutritions = nutrition.search([])
        print("---------------------------------------")
        print(len(nutritions))
        for rec in nutritions:

            print('rec.name:  ', rec.name)
            print('rec.name2:  ', rec.name2)
            rec.name = rec.name2
        return True

    # @api.model
    # def recompute_vat_price_tax(self):
    #     invoice_env = self.env["account.invoice.line"]
    #     invoices = invoice_env.search([])
    #     self.env.add_todo(invoice_env._fields["vat_price_tax"], invoices)
    #     self.env.add_todo(invoice_env._fields["vat_price_subtotal"], invoices)
    #     invoice_env.recompute()
    #     return True

