from odoo import models, fields, api
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class EnrollWizard(models.TransientModel):

    _name = 'faculty.enroll_wizard'
    _description = 'Permite establecer fecha de validacion'

    course_id = fields.Many2one('faculty.course', string='Curso')
    credits_required =  fields.Integer(string='Creditos necesarios', related="course_id.credits_required")


    def action_enroll(self):
        if self.course_id: 
            vals = {}
            student = self.env['faculty.student'].browse(self._context.get('student_id'))
            if student.qty_credits >= self.course_id.credits_required:
                vals['qty_credits'] = student.qty_credits - self.course_id.credits_required
                vals['course_ids'] = [(4, self.course_id.id)]
            if vals:
                student.write(vals)
                message="Se ha matriculado en el curso {}".format(self.course_id.name)
                student.message_post(body=message, subtype="mail.mt_note")
            else:
                raise ValidationError("No cuenta con suficientes c'reditos para matricular en este curso")
            return True