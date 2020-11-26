from odoo import models, fields, api
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class CourseGlobalScoreWizard(models.TransientModel):

    _name = 'faculty.course_global_score_wizard'
    _description = 'Permite establecer fecha de validacion'
    
    course_id = fields.Many2one('faculty.course', string='Curso', domain="[('is_my_course','=',True),('id','in',course_ids)]", required = True)
    mark = fields.Float(string='Nota global', digits=(5,2), required=True)
    student_id = fields.Many2one('faculty.student', string='')
    course_ids = fields.Many2many('faculty.course', string='', related="student_id.course_ids")
    @api.model
    def default_get(self, field_names):
        defaults = super(CourseGlobalScoreWizard, self).default_get(field_names)
        defaults['student_id'] = self._context.get('student_id')
        return defaults



    def action_set_mark(self):
        if self.course_id and self.mark: 
            vals = {}
            student = self.env['faculty.student'].browse(self._context.get('student_id'))
            course_student_mark = self.env['faculty.course_student_mark']
            mark_exists = course_student_mark.search([('student_id','=',student.id),('course_id','=',self.course_id.id)])
            vals['mark'] = self.mark
            if mark_exists:
                mark_exists.write(vals)
            else:
                vals['student_id'] = student.id
                vals['course_id'] = self.course_id.id
                course_student_mark.create(vals)
        else:
            raise ValidationError("Debe suministrar los datos")
        return True