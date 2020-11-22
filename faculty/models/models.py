# -*- coding: utf-8 -*-

from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

# class faculty(models.Model):
#     _name = 'faculty.faculty'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Course(models.Model):
    _name = 'faculty.course'
    _description = 'Allows to manage the information about courses'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Char(string='Descripción', required=True)
    credits_required = fields.Integer(string='Creditos necesarios', required=True)
    #profesor_ids = fields.Many2many('res.users', string='Profesores')
    #student_ids =  fields.Many2many('res.users', string='Estudiantes')

class Student(models.Model):
    _name = 'faculty.student'
    _description = 'Allows to manage the students information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required= True)
    
    qty_credits = fields.Integer(string='Creditos', required=True)
    
    identification = fields.Char(string='Carnet de Identidad', required =True, copy=False)
    _sql_constraints = [
        ('identification_unique',
         'UNIQUE(identification)',
         "Ya existe un estudiante con el mismo carnet de identidad"),
         ('cedula_check_lenght', 'check (LENGTH(identification) = 11)',
         "El carnet de identidad debe contener 11 números"),  
    ]
    image = fields.Binary(
        "Foto",
        attachment=True,
        help=
        "Campo para la foto del estudiante, dimensión máxima 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True)
    image_small = fields.Binary("Small-sized photo", attachment=True)   

    gender = fields.Selection([
        ('male', 'Hombre'),
        ('female','Mujer')
    ], string='Genero', required=True, default='male')
    date_birthday = fields.Date(string='Fecha de nacimiento', required=True)
    email = fields.Char(string='Correo electrónico')
    phone = fields.Char(string='Celular')

    @api.model
    def _get_default_image(self):
        image_path = get_module_resource('faculty',
                                         'static/src/img', 'default_image.png')
        with open(image_path, 'rb') as f:
            image = f.read()
        if image:
            image = tools.image_colorize(image)
        return tools.image_resize_image_big(
            base64.b64encode(image))

    course_ids = fields.Many2many('faculty.course', string='Cursos')

    age = fields.Integer(compute='_compute_age', string='Edad', store=True)
    
    @api.one
    @api.depends('date_birthday')
    def _compute_age(self):
        for record in self:
            if record.date_birthday:    
                today = fields.Date.today()
                offset = int(self.date_birthday.replace(year=today.year) > today)  # int(True) == 1, int(False) == 0
                record.age = today.year - self.date_birthday.year - offset  

    @api.onchange('user_id')
    def _onchange_user(self):
        if self.user_id:
            self.update(self._sync_user(self.user_id))

    def _sync_user(self, user):
        vals = dict(
            name=user.name,
            image=user.image,
            email=user.email,
        )
        #if user.tz:
        #    vals['tz'] = user.tz
        return vals  

    @api.model
    def create(self, vals):
        if not vals.get('image'):
            vals['image'] = self._get_default_image()
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        
        tools.image_resize_images(vals)
        employee = super(Student, self).create(vals)
        return employee

    @api.multi
    def write(self, vals):
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        tools.image_resize_images(vals)
        res = super(Student, self).write(vals)
        return res
    
    def action_enroll(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Matricular',
            'res_model': 'faculty.enroll_wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context':{'student_id':self.id},
            'target': 'new',
        }
        return action
    

"""
class Student(models.Model):
    name = 'faculty.student'
    _description = 'Allows to manage the students information'

    qty_credits = fields.Integer(string='Creditos', required=True)
    
    identification = fields.Char(string='Carnet de Identidad', required =True, copy=False)
    _sql_constraints = [
        ('identification_unique',
         'UNIQUE(identification)',
         "Ya existe un estudiante con el mismo carnet de identidad"),
         ('cedula_check_lenght', 'check (LENGTH(identification) = 11)',
         "El carnet de identidad debe contener 11 números"),  
    ]
    user_id = fields.Many2one('res.', string='')

class Student(models.Model):
    #_name = 'module.name'
    _description = 'Allows to manage the students information'

    _inherit = "res.users"

    qty_credits = fields.Integer(string='Creditos', required=True)
    
    identification = fields.Char(string='Carnet de Identidad', required =True, copy=False)

    course_ids = fields.Many2many('res.users', string='Cursos')
    

class Course(models.Model):
    _name = 'faculty.course'
    _description = 'Allows to manage the information about courses'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Char(string='Descripción', required=True)
    credits_required = fields.Integer(string='Creditos necesarios', required=True)
    profesor_ids = fields.Many2many('res.users', string='Profesores')
    student_ids =  fields.Many2many('res.users', string='Estudiantes')
        
"""
    