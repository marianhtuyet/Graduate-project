from odoo import _, api, fields, models


class Student(models.Model):
    _name = 'student'

    holy_name = fields.Char()
    first_name = fields.Char()
    last_name = fields.Char()
    name = fields.Char(compute='_compute_name')
    code = fields.Char('ID')
    date_of_birth = fields.Char()
    position_of_birth = fields.Char()
    congregation = fields.Char()
    congregation2 = fields.Many2one('congregation', 'Congregation2')
    study_class_ids = fields.One2many('study.class', 'student_id')
    school_year_id = fields.Many2one('school.year', 'School year', required=True)

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name =  '{} {}'.format(
                rec.last_name if rec.last_name else '' ,
                rec.first_name if rec.first_name else ''
            )

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.first_name if rec.first_name else 'Name' + ' ' + rec.last_name if rec.last_name else 'Name'
            result.append((rec.id, name))
        return result

    @api.multi
    def add_all_subject(self):
        study_class_env = self.env['study.class']
        subject_env = self.env['subject']
        for rec in self:
            list_subject = subject_env.search([]) ##get all subject
            for subject in list_subject:
               study_class = study_class_env.create({
                    'subject_id': subject.id,
                    'student_id':  rec.id,
                    'first_test': 0,
                    'units': subject.units
               })
        return True


    def print_report_transcript_report(self):
        self.ensure_one()
        return self.env.ref(
                'Caculate_score.student_score_report').report_action(self.id)

