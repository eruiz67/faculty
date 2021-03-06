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

    @api.constrains('credits_required')
    def _constrains_credits_required(self):
        for record in self:
             if record.qty_credits < 0:                
	             raise ValidationError("La cantidad de créditos asignados debe ser mayor o igual a cero")

    #profesor_ids = fields.Many2many('res.users', string='Profesores')
    student_ids =  fields.Many2many('faculty.student', string='Estudiantes')
    professor_ids  = fields.Many2many('faculty.professor', string='Profesores')
    def action_enroll(self, parameter_list):
        vals={}
        if self.env.user.student_ids:
            student = self.env.user.student_ids[0]
            if self.id in student.course_ids.ids:
                raise ValidationError("Usted ya se encuentra matriculado en este curso")
            if student.qty_credits >= self.credits_required:
                vals['qty_credits'] = student.qty_credits - self.credits_required
                vals['course_ids'] = [(4, self.id)]
            if vals:
                student.sudo().write(vals)
                print("Se ha matriculado en el curso")
                #message="Se ha matriculado en el curso {}".format(self.name)
                #student.message_post(body=message, subtype="mail.mt_note")
            else:
                raise ValidationError("No cuenta con suficientes c'reditos para matricular en este curso")
            return True
    
    is_user_enrolled = fields.Boolean(compute='_compute_is_user_enrolled', string='Esta matriculado?')
    
    def action_quit(self):
        vals={}
        if self.env.user.student_ids:
            student = self.env.user.student_ids[0]
            if self.id not in student.course_ids.ids:
                raise ValidationError("Usted no se encuentra matriculado en este curso")
            else:
                vals['course_ids'] = [(3, self.id)]
                student.sudo().write(vals)
                message="Ha canselado la matricula del curso {}".format(self.name)
                student.message_post(body=message, subtype="mail.mt_note")

        return True

    def _compute_is_user_enrolled(self):
        is_student = self.env.user.student_ids
        if is_student:
            student = self.env.user.student_ids[0]
            for record in self:
                if student and record.id in student.course_ids.ids:
                    record.is_user_enrolled =  True
                else:
                    record.is_user_enrolled =  False
        else:
            for record in self:
                record.is_user_enrolled =  False

    is_user_professor = fields.Boolean(compute='_compute_is_user_professor', string='Eres profesor?')
    

    def _compute_is_user_professor(self):
        is_professor = self.env.user.professor_ids
        if is_professor:
            professor = self.env.user.professor_ids[0]
            for record in self:
                if professor and record.id in professor.course_ids.ids:
                    record.is_user_professor =  True
                else:
                    record.is_user_professor =  False
        else:
            for record in self:
                record.is_user_professor =  False

    

    is_my_course = fields.Boolean(compute='_compute_is_my_course', search='_search_is_my_course',string='Es mi curso?')
    
    def _compute_is_my_course(self):
        is_professor = self.env.user.professor_ids
        is_student = self.env.user.student_ids
        if is_professor:
            professor = self.env.user.professor_ids[0]
            for record in self:
                if professor and record.id in professor.course_ids.ids:
                    record.is_my_course =  True
                else:
                    record.is_my_course =  False
        elif is_student:
            student = self.env.user.student_ids[0]
            for record in self:
                if student and record.id in student.course_ids.ids:
                    record.is_my_course =  True
                else:
                    record.is_my_course =  False
        else:
            for record in self:
                record.is_my_course =  False

    def _search_is_my_course(self, operator, value):
        courses = self.env['faculty.course'].search([])
        list_courses=[]
        for rec in courses:
            if rec.is_my_course:
                list_courses.append(rec.id)
        return [('id','in', list_courses)]
    
    exam_ids = fields.One2many('faculty.exam', 'course_id', string='Examenes')
    course_student_mark_ids =  fields.One2many('faculty.course_student_mark', 'course_id', string='Notas')

    course_student_mark = fields.Float(compute='_compute_course_student_mark', string='Nota',  digits=(5, 2))


    def _compute_course_student_mark(self):
        for rec in self:
            if self.env.user.student_ids and self.env.user.student_ids[0] :
                qualified = self.env['course_student_mark'].search([('course_id','=',rec.id ),('student_id','=', self.env.user.student_ids[0].id)],limit=1)
                if qualified:
                    rec.course_student_mark = qualified.mark


class Student(models.Model):
    _name = 'faculty.student'
    _description = 'Allows to manage the students information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required= True, domain="[('student_ids','=',False),('is_faculty_student','=',True)]")
    
    qty_credits = fields.Integer(string='Creditos', required=True)
    
    identification = fields.Char(string='Carnet de Identidad', required =True, copy=False)

    @api.constrains('identification')
    def _check_identification (self):
        # otra podria ser "[^@]+@[^@]+\.[^@]+"
        for record in self:
             if record.identification and not re.match(r"(^[\d]+$)", record.identification):                
	             raise ValidationError("El carnet de identidad debe contener 11 números")

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
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Student, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='date_birthday']"):
                node.set('options', "{'datepicker': {'maxDate': '%sT23:59:59'}}" % fields.Date.today().strftime(DEFAULT_SERVER_DATE_FORMAT))
            res['arch'] = etree.tostring(doc)
        return res 


    @api.constrains('date_birthday')
    def _constrains_birthday(self):
        for record in self:
            if record.date_birthday and record.date_birthday > fields.Date.today():
                raise ValidationError("La fecha de nacimiento debe ser anterior a la fecha actual")

    @api.constrains('qty_credits')
    def _constrains_qty_credits(self):
        for record in self:
             if record.qty_credits < 0:                
	             raise ValidationError("La cantidad de créditos requeridos debe ser mayor o igual a cero")
                

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
    course_student_mark_ids =  fields.One2many('faculty.course_student_mark', 'student_id', string='Notas')


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

    professor_ids = fields.Many2many(comodel_name='faculty.professor',
                                  delete="cascade",
                                  compute="_compute_professor_ids")
    @api.one
    def _compute_professor_ids(self):
        #self.env.cr.execute

        self._cr.execute("""
                SELECT professor.id, professor.name, student.name, course.name 
                from faculty_student student 
                JOIN faculty_course_faculty_student_rel cs
                ON (student.id=cs.faculty_student_id)
                JOIN faculty_course course
                    ON (cs.faculty_course_id = course.id) 
                JOIN faculty_course_faculty_professor_rel cp
                ON (cp.faculty_course_id=course.id)  
                JOIN faculty_professor professor 
                    ON (professor.id = cp. faculty_professor_id) 
                where student.id={};
            """.format(self.id))
        res = self._cr.fetchall()
        professor_list=[]
        if res:
            for professor in res:
                print("{} con id es {}".format(professor[1],professor[0]))
                professor_list.append(int(professor[0]))
                
            self.professor_ids=self.env['faculty.professor'].sudo().browse(professor_list) 
    

    @api.multi
    def action_qualify_student(self):

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Enviar respuesta',
            'res_model': 'faculty.course_global_score_wizard',
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

class CourseStudentMark(models.Model):
    _name = 'faculty.course_student_mark'
    _description = 'Allows to set a global score for a couse to a student'

    course_id = fields.Many2one('faculty.course', string='Curso')
    student_id = fields.Many2one('faculty.student', string='Estudiante')

    mark = fields.Float(string='Nota global', digits=(5,2))

    