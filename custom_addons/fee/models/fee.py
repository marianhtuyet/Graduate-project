import calendar
from odoo import models, fields, api


class Fee(models.Model):
    _name = 'student.fee'

    def _last_business_day_in_month(self):
        current_date = fields.Date.today()
        array_temp =  calendar.monthcalendar(current_date.year, current_date.month)
        array_result = [item[0:5] for item in array_temp]
        count_date = 0
        for item in array_result:
            for i in item:
                count_date += 1 if i > 0 else 0
        return count_date

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
    date_study = fields.Integer('Số ngày', default=_last_business_day_in_month)
    student_name = fields.Char(
        'Tên học sinh',
        related='student_id.student_name'
    )
    date_absent = fields.Integer('Số ngày vắng')
    date_submit = fields.Date('Ngày nộp đến', default=fields.Date.today)
    date_to = fields.Date('Ngày đến', default=fields.Date.today)
    date_apply = fields.Date('Ngày áp dụng', default=fields.Date.today)
    month_submit = fields.Char('Tháng thu', compute='compute_month_submit', store=True)
    user_id = fields.Many2one(
        'res.users', "Người thu",
        default=lambda self: self.env.uid)
    line_ids = fields.One2many('fee.line.detail', 'fee_id')
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company_id.currency_id.id
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
    reduce_code = fields.Float("Tỉ lệ miễn giảm %")
    state = fields.Selection(
        [('unpaid', 'Chưa thu'),
         ('paid', 'Đã thu'),
        ])
    printed = fields.Boolean('Printed')

    def name_get(self):
        list_name = []
        for rec in self:
            name = "{} - {}".format('Học phí', rec.student_name if rec.student_name else '')
            list_name.append((rec.id, name))
        return list_name

    @api.depends('date_submit')
    def compute_month_submit(self):
        for rec in self:
            rec.month_submit = str(rec.date_submit.month) + ' / '+ str(rec.date_submit.year) \
                if rec.date_submit else 0

    @api.depends('line_ids.amount', 'date_absent', 'date_study')
    def _compute_total_amount(self):
        for rec in self:
            daily_fee = sum(line.amount for line in  rec.line_ids.filtered(lambda m: m.fee_detail.type_fee == 1))
            rec.total_amount = sum(line.amount for line in rec.line_ids.filtered(
                lambda m: m.fee_detail.type_fee in (2,3))) + daily_fee*rec.date_study
            rec.total_absent = daily_fee * rec.date_absent
            rec.total_submit = (rec.total_amount - rec.total_absent)*(
                1 - rec.student_id.reduce_code.amount if rec.student_id.reduce_code else 0)

    @api.multi
    def do_print_fee_notify(self):
        self.write({'printed': True})
        return self.env.ref('fee.action_report_notify').report_action(self)

    @api.multi
    def do_print_fee_receipt(self):
        self.write({'printed': True})
        return self.env.ref('fee.action_report_receipt').report_action(self)

    @api.multi
    def add_all_fee(self):
        fee_detail_env = self.env['fee.detail']
        fee_line_detail = self.env['fee.line.detail']
        for rec in self:
            list_fee_detail = fee_detail_env.search([('type_fee', 'in', (1, 2)), ('status', '=', 1)])

            for fee_detail in list_fee_detail:
                detail = fee_line_detail.create({
                    'fee_id': rec.id,
                    'fee_detail': fee_detail.id,
                    'amount': fee_detail.amount,
                    'currency_id': fee_detail.currency_id.id,
                    'type_fee': 1
                })
        return True

    @api.onchange('student_id')
    def onchange_student_id(self):
        for rec in self:
            rec.reduce_code = rec.student_id.reduce_code.amount*100 or 0

    @api.multi
    def add_all_skill(self):
        fee_detail_env = self.env['fee.detail']
        fee_line_detail = self.env['fee.line.detail']
        for rec in self:
            list_fee_detail = fee_detail_env.search([('type_fee', '=', 3), ('status', '=', 1)])
            for fee_detail in list_fee_detail:
                detail = fee_line_detail.create({
                    'fee_id': rec.id,
                    'fee_detail': fee_detail.id,
                    'amount': fee_detail.amount,
                    'currency_id': fee_detail.currency_id.id,
                    'type_fee': 1
                })
        return True



