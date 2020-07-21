from odoo import api, fields, models


class StudyClass(models.Model):
    _name = 'study.class'

    school_year_id = fields.Many2one('school.year')
    subject_id = fields.Many2one('subject', required=True)
    student_id = fields.Many2one('student', required=True)
    units = fields.Integer()
    first_test = fields.Float(default=0.0, required=True)
    second_test = fields.Float(default=0.0)
    third_test = fields.Float(default=0.0)
    grade_point = fields.Float()
    qualification = fields.Char(compute='_compute_qualification')

    @api.depends('grade_point')
    def _compute_qualification(self):
        for rec in self:
            if rec.grade_point >  1.0 and rec.grade_point <= 1.2:
                rec.qualification = 'E'
            elif rec.grade_point <= 1.45:
                rec.qualification = 'VG'
            elif rec.grade_point <= 1.85:
                rec.qualification = 'G'
            elif rec.grade_point <= 2.4:
                rec.qualification = 'F'
            elif rec.grade_point <= 3.0:
                rec.qualification = 'P'
            else:
                rec.qualification = 'F'

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = '%s - %s' % (rec.student_id.name, rec.school_year_id.name)
            res.append(name if name else 'Detail Draft')
        return res

