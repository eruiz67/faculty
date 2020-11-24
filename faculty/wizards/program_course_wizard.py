from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

class EnrollWizard(models.TransientModel):

    _name = 'faculty.program_course_wizard'
    _description = 'Permite establecer fecha de validacion'

    date_published = fields.Datetime(string='Fecha de publicacion', required=True)

    def action_program(self):
        vals = {}
        exam = self.env['faculty.exam'].browse(self._context.get('exam_id'))
        if self.date_published < fields.Datetime.now():
            raise ValidationError("La fecha y hora de publicación debe ser menor a la fecha y hora actual")
        else:
            vals['date_published'] = self.date_published
            vals['state'] = 'waiting'
            exam.write(vals)