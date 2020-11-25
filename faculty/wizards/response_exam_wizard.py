from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import logging

class ResponseExamWizard(models.TransientModel):

    _name = 'faculty.response_exam_wizard'
    _description = 'Allows to submit a response for an exam'

    file_response =  fields.Binary(string='Adjunto')
    filename =  fields.Char()
    response_description = fields.Text(string='Descripcion')
    
    def action_response_exam(self):
        vals={}
        exam = self.env['faculty.exam'].browse(self._context.get('exam_id'))
        vals['student_id'] = self.env.user.student_id_computed.id
        if exam.response_ids:
            for rec in exam.response_ids:
                if rec.student_id.id == self.env.user.student_id_computed.id:
                    raise ValidationError("Ustade ya ha enviado una respuesta para el presente examen")
                
        vals['exam_id'] = exam.id
        vals['response_description'] = self.response_description
        vals['filename'] = self.filename
        # How to pass this binary field to the write method
        vals['file_response'] = self.file_response
        
        response = self.env['faculty.response']
        response.create(vals)
