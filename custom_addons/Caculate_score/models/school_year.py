from odoo import _, api, fields, models


class SchoolYear(models.Model):
    _name = 'school.year'

    name = fields.Char()
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
