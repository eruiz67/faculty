from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

class ResUsersStudent(models.Model):
    _inherit = "res.users"
    _description = 'Adds a student field to the user and professor'

    student_ids = fields.One2many('faculty.student', 'user_id', string='Estudiante')
    professor_ids = fields.One2many('faculty.professor', 'user_id', string='Profesor')