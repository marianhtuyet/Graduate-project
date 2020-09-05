from odoo import api, fields, models


class StudyClass(models.Model):
    _name = 'study.class'

    school_year_id = fields.Many2one('school.year')
    subject_id = fields.Many2one('subject', required=True)
    student_id = fields.Many2one('student', required=True)
    units = fields.Integer(default=0)
    first_test = fields.Float(default=0.0, required=True)
    second_test = fields.Float(default=0.0)
    third_test = fields.Float(default=0.0)
    grade_point = fields.Float()
    qualification = fields.Char(compute='_compute_qualification')

    @api.depends('grade_point')
    def _compute_qualification(self):
        for rec in self:
            if 1.0 <= rec.grade_point <= 1.2:
                rec.qualification = 'E'
            elif 1.2 < rec.grade_point <= 1.45:
                rec.qualification = 'VG'
            elif 1.45 < rec.grade_point <= 1.85:
                rec.qualification = 'G'
            elif 1.85 < rec.grade_point <= 2.4:
                rec.qualification = 'F'
            elif 2.4 < rec.grade_point <= 3.0:
                rec.qualification = 'P'
            else:
                rec.qualification = 'F'
