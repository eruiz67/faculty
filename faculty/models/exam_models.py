from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class Exam(models.Model):
    _name = 'faculty.exam'
    _inherits = {'ir.attachment': 'attachment_id'}
    _description = 'Allows professor to create exams'

    
    description = fields.Char(string='Descripcion')
    datas = fields.Binary(string='Archivo',required=True)
    date_published  =  fields.Datetime(string='Fecha de publicacion')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('waiting', 'Programado'),
        ('published', 'Publicado'),
        ('cancelled','Cancelado')
    ], string='Estado',default="draft")

    @api.multi
    def action_program(self):
        self.state = 'waiting'


    @api.multi
    def action_publish(self):
        self.ensure_one()
        self.state = 'published'
        #self.write({'state': 'solicitado'})

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancelled'
        #self.write({'state': 'solicitado'})

    """
    is_published = fields.Char(compute='_compute_is_published', string='Esta publicado')
    
    @api.depends('date_published')
    def _compute_is_published(self):
        pass
    """

    course_id = fields.Many2one('faculty.course', string='Curso', domain="[('is_my_course','=',True)]", help="Curso al que pertenece el examen. Un profesor solamente podra crear examenes para los cursos que imparte")

"""
class Response(models.Model):
    _name = 'faculty.response'
    _description = 'Allows student to submit responses'


    exam_is = fields.Many2one('faculty.exam', string='Examen')
    student_id = fields.Many2one('faculty.student', string='Estudiante')
    response_file = fields.Binary(string='Respuesta')
    exam_filename = fields.Char()
    response_description = fields.Text(string='Descripcion')
    mark = fields.Float(string='Nota', digits=(5,2))
"""

class Response(models.Model):
    _name = 'faculty.response'
    _description = 'Allows student to submit responses'
    _inherits = {'ir.attachment': 'attachment_id'}

    datas = fields.Binary(string='Archivo',required=True)
    exam_id = fields.Many2one('faculty.exam', string='Examen')
    student_id = fields.Many2one('faculty.student', string='Estudiante')

    response_description = fields.Text(string='Descripcion')
    mark = fields.Float(string='Nota', digits=(5,2))
