from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

class Professor(models.Model):
    _name = 'faculty.professor'
    _description = 'Allows to manage the professors information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required= True, domain="[('professor_ids','=',False)]")
        
    identification = fields.Char(string='Carnet de Identidad', required =True, copy=False)
    _sql_constraints = [
        ('identification_unique',
         'UNIQUE(identification)',
         "Ya existe un profesor con el mismo carnet de identidad"),
         ('cedula_check_lenght', 'check (LENGTH(identification) = 11)',
         "El carnet de identidad debe contener 11 números"),  
    ]
    image = fields.Binary(
        "Foto",
        attachment=True,
        help=
        "Campo para la foto del profesor, dimensión máxima 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True)
    image_small = fields.Binary("Small-sized photo", attachment=True)   

    gender = fields.Selection([
        ('male', 'Hombre'),
        ('female','Mujer')
    ], string='Género', required=True, default='male')
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

    course_ids = fields.Many2many('faculty.course', string='Cursos impartidos')

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
        professor = super(Professor, self).create(vals)
        return professor

    @api.multi
    def write(self, vals):
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        tools.image_resize_images(vals)
        professor = super(Professor, self).write(vals)
        return professor

    
    student_ids = fields.Many2many(comodel_name='faculty.student',
                                  delete="cascade",
                                  compute="_compute_student_ids")
    @api.one
    def _compute_student_ids(self):
        #self.env.cr.execute

        self._cr.execute("""
                SELECT student.id, student.name, professor.name, course.name 
                from faculty_student student 
                JOIN faculty_course_faculty_student_rel cs
                ON (student.id=cs.faculty_student_id)
                JOIN faculty_course course
                    ON (cs.faculty_course_id = course.id) 
                JOIN faculty_course_faculty_professor_rel cp
                ON (cp.faculty_course_id=course.id)  
                JOIN faculty_professor professor 
                    ON (professor.id = cp. faculty_professor_id) 
                where professor.id={};
            """.format(self.id))
        res = self._cr.fetchall()
        student_list=[]
        if res:
            for student in res:
                print("{} con id es {}".format(student[1],student[0]))
                student_list.append(int(student[0]))
                
            self.student_ids=self.env['faculty.student'].sudo().browse(student_list) 
    
