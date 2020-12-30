from datetime import date
from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.exceptions import UserError


class StudentStudent(models.Model):
    _inherit = 'student.student'

    reduce_code = fields.Many2one('fee.reduce', 'Mã miễn giảm')
    customize_code = fields.Char('Mã học sinh')
    custom_name = fields.Char('Tên học sinh')
    father_name = fields.Char('Tên Cha')
    father_job = fields.Char('Nghề nghiệp Cha')
    mother_name = fields.Char('Tên Mẹ')
    mother_job = fields.Char('Nghề nghiệp Mẹ')
    phone_father = fields.Char('SĐT Cha')
    phone_mother = fields.Char('SĐT Mẹ')

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = '{} - {}'.format(rec.customize_code, rec.custom_name)
            result.append((rec.id, name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        invoice_ids = []
        # domain = args + ['|', ('custom_name', operator, name), ('customize_code', operator, name)]
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            connector = '&' if operator in expression.NEGATIVE_TERM_OPERATORS else '|'
            domain = [connector, ('custom_name', operator, name), ('customize_code', operator, name)]
        journal_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(journal_ids).name_get()

    def unlink(self):
        fees = self.env['student.fee'].search([('student_id', 'in', self.ids)])
        if fees:
            raise UserError(_('Students have fee, cannot delete.'))
        # With the non plannified picking, draft moves could have some move lines.
        return super(StudentStudent, self).unlink()
