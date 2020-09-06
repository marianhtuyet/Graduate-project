from datetime import date
from odoo import models, fields, api


class Fee(models.Model):
    _name = 'student.fee'

    student_id = fields.Many2one(
        'student.student',
        'Mã học sinh',
        required=True
    )
    student_code = fields.Char(
        'Mã học sinh',
        related='student_id.student_code'
    )
    standard_id = fields.Many2one(
        'school.standard',
        'Lớp học',
        related='student_id.standard_id'
    )
    date_study = fields.Integer('Số ngày')
    student_name = fields.Char(
        'Tên học sinh',
        related='student_id.student_name'
    )
    date_absent = fields.Integer('Số ngày vắng')
    date_submit = fields.Date('Ngày nộp đến')
    date_to = fields.Date('Ngày đến')
    date_apply = fields.Date('Ngày áp dụng')
    month_submit = fields.Char('Tháng thu', compute='compute_month_submit')
    user_id = fields.Many2one(
        'res.users', "Người thu",
        default=lambda self: self.env.uid)
    line_ids = fields.One2many('fee.line.detail', 'fee_id')
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.user.company_id.currency_id.id
    )

    total_amount = fields.Monetary(
        'Tổng tiền thu',
        compute='_compute_total_amount',
        currency_field='currency_id'
    )
    total_absent = fields.Monetary(
        'Số tiền vắng',
        compute='_compute_total_amount',
        currency_field='currency_id'
    )
    total_submit = fields.Monetary(
        'Tổng tiền thu thực',
        compute='_compute_total_amount',
        currency_field='currency_id'
    )

    @api.depends('date_submit')
    def compute_month_submit(self):
        for rec in self:
            rec.month_submit = str(rec.date_submit.month) + ' / '+ str(rec.date_submit.year) \
                if rec.date_submit else 0

    @api.multi
    def add_all_fee(self):
        fee_detail_env = self.env['fee.detail']
        fee_line_detail = self.env['fee.line.detail']
        for rec in self:
            list_fee_detail = fee_detail_env.search([('status', '=', 1)])
            for fee_detail in list_fee_detail:
                detail = fee_line_detail.create({
                    'fee_id': rec.id,
                    'fee_detail': fee_detail.id,
                    'name': fee_detail.name,
                    'amount': fee_detail.amount,
                    'currency_id': fee_detail.currency_id.id,
                    'type_fee': 1
                })
        return True

    def name_get(self):
        list_name = []
        for rec in self:
            name = "{} - {}".format('Học phí', rec.student_name if rec.student_name else '')
            list_name.append((rec.id, name))
        return list_name

    @api.depends('line_ids.amount', 'date_absent', 'date_study')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(line.amount for line in rec.line_ids)
            rec.total_absent = rec.total_amount * rec.date_absent/ rec.date_study if rec.date_study !=0 else 0
            rec.total_submit = rec.total_amount - rec.total_absent

