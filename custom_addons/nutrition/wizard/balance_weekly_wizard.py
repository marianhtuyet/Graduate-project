from odoo import _, api, fields, models
from odoo.exceptions import UserError
import datetime
from datetime import timedelta, date


class NutritionBalanceWizard(models.TransientModel):
    _name = 'nutrition.balance.wizard'
    _description = 'nutrition.balance.wizard'

    date_from = fields.Date(required=True, default= date.today() + timedelta(days= -date.today().weekday()))
    date_to = fields.Date(compute='_compute_date_to')
    nutrition_ids = fields.Many2many(
        comodel_name='modify.menu.food',
        string='Điều chỉnh thực đơn',
        # domain="[('user_type_id.name', '=', 'Bank and Cash')]",
    )


    @api.multi
    def print_xlsx_report(self):
        self.ensure_one()
        if self.date_from.weekday() != 0:
            raise UserError(_("Ngày bắt đầu phải là thứ 2!"))
        return self.env.ref('nutrition.nutrition_balance_xlsx'
                            ).report_action(self)

    @api.depends('date_from')
    def _compute_date_to(self):
        for rec in self:
            rec.date_to = rec.date_from + timedelta(days=-rec.date_from.weekday() + 4)

    @api.onchange('date_from')
    def onchange_date_from(self):
        for rec in self:
            rec.date_to = rec.date_from + timedelta(days=-rec.date_from.weekday() + 4)
