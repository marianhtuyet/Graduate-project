from odoo import _, api, fields, models


class Student(models.Model):
    _name = 'student'

    holy_name = fields.Char()
    first_name = fields.Char()
    last_name = fields.Char()
    name = fields.Char()
    code = fields.Char('ID')
    date_of_birth = fields.Char()
    position_of_birth = fields.Char()
    congregation = fields.Char()

    study_class_ids = fields.One2many('study.class', 'student_id')

    @api.onchange('first_name', 'last_name')
    def onchange_name(self):
        for rec in self:
            rec.name = \
                rec.first_name if rec.first_name \
                    else '' + rec. last_name if rec.last_name else ''

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.first_name + ' ' + rec.last_name
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
               })
        return True

