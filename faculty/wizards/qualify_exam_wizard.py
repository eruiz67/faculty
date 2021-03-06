from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import logging

class QualifyExamWizard(models.TransientModel):

    _name = 'faculty.qualify_exam_wizard'
    _description = 'Allows to qualify a response for an exam'

    mark = fields.Float(string='Nota', digits=(5,2))
    comments = fields.Text(string='Comentarios')

    @api.constrains('mark')
    def _constrains__mark(self):
        for record in self:
             if record.mark < 0 or record.mark>100:                
	             raise ValidationError("La nota debe ser un valor entre  0 y 100")

    def action_qualify_exam(self):
        vals={}
        exam = self.env['faculty.response'].browse(self._context.get('response_id'))
        vals['mark'] = self.mark
        vals['comments'] = self.comments
        vals['state'] = 'qualified'
        exam.sudo().write(vals)