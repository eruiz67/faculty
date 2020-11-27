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

    student_id_computed = fields.Many2one(comodel_name='faculty.student',compute='_compute_student_id_computed', string='Estudiante')
    

    @api.depends('student_ids')
    def _compute_student_id_computed(self):
        for rec in self:
            if rec.student_ids:
                rec.student_id_computed = self.env['faculty.student'].browse(rec.student_ids[0].id)

    professor_id_computed = fields.Many2one(comodel_name='faculty.professor',compute='_compute_professor_id_computed', string='Profesor')
    

    @api.depends('professor_ids')
    def _compute_professor_id_computed(self):
        for rec in self:
            if rec.professor_ids:
                rec.professor_id_computed = self.env['faculty.professor'].browse(rec.professor_ids[0].id)



    is_faculty_student = fields.Boolean(compute='_compute_is_faculty_student', search="_search_is_faculty_student", string='Es estudiante?')
    
    def _compute_is_faculty_student(self):
        for rec in self:
            rec.is_faculty_student = rec.has_group("faculty.group_faculty_student") and not rec.has_group("faculty.group_faculty_professor") and not rec.has_group("faculty.group_faculty_admin")
    
    
    def _search_is_faculty_student(self, operator, value):
        users = self.env['res.users'].sudo().search([])
        list_users=[]
        for rec in users:
            if rec.has_group("faculty.group_faculty_student") and not rec.has_group("faculty.group_faculty_professor") and not rec.has_group("faculty.group_faculty_admin"):
                list_users.append(rec.id)
        return [('id','in', list_users)]

    is_faculty_professor = fields.Boolean(compute='_compute_is_faculty_student', search="_search_is_faculty_professor", string='Es profesor?')
    
    def _compute_is_faculty_professor(self):
        for rec in self:
            rec.is_faculty_professor = rec.has_group("faculty.group_faculty_professor") and not rec.has_group("faculty.group_faculty_student") and not rec.has_group("faculty.group_faculty_admin")
    
    
    def _search_is_faculty_professor(self, operator, value):
        users = self.env['res.users'].sudo().search([])
        list_users=[]
        for rec in users:
            if rec.has_group("faculty.group_faculty_professor") and not rec.has_group("faculty.group_faculty_student") and not rec.has_group("faculty.group_faculty_admin"):
                list_users.append(rec.id)
        return [('id','in', list_users)]