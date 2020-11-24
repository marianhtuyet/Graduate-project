from datetime import timedelta, date, datetime
from odoo import api, fields, models
# models.TransientModel


class MenuAutomaticWeekly(models.Model):
    _name = 'menu.automatic.weekly'
    _description = 'Thực đơn tự động tuần'

    date_start = fields.Date(required=True, default= date.today() + timedelta(days= -date.today().weekday()))
    date_end = fields.Date(compute='_compute_date_end')
    name = fields.Char(compute='_compute_name')
    line_ids = fields.One2many('menu.automatic.weekly.line', 'menu_automatic_weekly_id')

    @api.depends('date_start')
    def _compute_date_end(self):
        for rec in self:
            rec.date_end = rec.date_start + timedelta(days=-rec.date_start.weekday() + 4)

    @api.onchange('date_start', 'date_end')
    def onchange_date_start(self):
        for rec in self:
            rec.date_end = rec.date_start + timedelta(days=-rec.date_start.weekday() + 4)
            rec.name = '{} - {}'.format(
                datetime.strptime(rec.date_start, "%Y-%m-%d"),
                datetime.strptime(rec.date_end, "%Y-%m-%d")
            )

    @api.depends('date_start', 'date_end')
    def _compute_name(self):
        for rec in self:
            rec.name = '{} - {}'.format(
                datetime.strptime(rec.date_start, "%Y-%m-%d"),
                datetime.strptime(rec.date_end, "%Y-%m-%d")
            )

    def create_menu_automatic(self):
        print("1"*80)
        return True
