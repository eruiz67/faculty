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


    is_faculty_student = fields.Boolean(compute='_compute_is_faculty_student', search="_search_is_faculty_student", string='Es estudiante?')
    
    def _compute_is_faculty_student(self):
        for rec in self:
            rec.is_faculty_student = rec.has_group("faculty.group_faculty_student")
    
    
    def _search_is_faculty_student(self, operator, value):
        users = self.env['res.users'].sudo().search([])
        list_users=[]
        for rec in users:
            if rec.has_group("faculty.group_faculty_student"):
                list_users.append(rec.id)
        return [('id','in', list_users)]

    is_faculty_professor = fields.Boolean(compute='_compute_is_faculty_student', search="_search_is_faculty_professor", string='Es profesor?')
    
    def _compute_is_faculty_professor(self):
        for rec in self:
            rec.is_faculty_professor = rec.has_group("faculty.group_faculty_professor")
    
    
    def _search_is_faculty_professor(self, operator, value):
        users = self.env['res.users'].sudo().search([])
        list_users=[]
        for rec in users:
            if rec.has_group("faculty.group_faculty_professor"):
                list_users.append(rec.id)
        return [('id','in', list_users)]