from odoo import models, fields, tools, api, _
from odoo.modules.module import get_module_resource
import base64
import re
from odoo.exceptions import ValidationError
from lxml import etree
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
import logging


class Exam(models.Model):
    _name = 'faculty.exam'
    _description = 'Allows professor to create exams'

    name = fields.Char(string='Nombre')
    description = fields.Char(string='Descripcion')
    file_exam = fields.Binary(string='Adjunto',required=True)
    filename_exam =  fields.Char(string='')
    date_published  =  fields.Datetime(string='Fecha de publicacion')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('waiting', 'Programado'),
        ('published', 'Publicado'),
        ('cancelled','Cancelado')
    ], string='Estado',default="draft")

    @api.multi
    def action_program(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Programar',
            'res_model': 'faculty.program_course_wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context':{'exam_id':self.id},
            'target': 'new',
        }
        return action


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
    
    @api.multi
    def action_publish_cron(self):
        _logger = logging.getLogger(__name__)
        _logger.info("************ INICIANDO TAREA DE PUBLICACION DE EXAMENES ****************************")
        print("--------------------- INICIANDO TAREA DE PUBLICACION DE EXAMENES")
        exams = self.env['faculty.exam'].search([])
        for rec in exams:
            if rec.state =='waiting' and fields.datetime.now() >=fields.Datetime.now():
                rec.state = 'published'
                _logger.info("Se ha publicado el examen {} con id {}".format(rec.name, rec.id))
                print("Se ha publicado el examen {} con id {}".format(rec.name, rec.id))
        _logger.info("***********TAREA TERMINADA**********")
        print("-------- tarea terminada-------")
        return True

    response_ids = fields.One2many('faculty.response', 'exam_id', string='Respuestas')

    @api.multi
    def action_response_exam(self):
        context= dict(self.env.context)
        #context['form_view_initial_mode']='edit'
        context['exam_id']= self.id
        context['student_id'] = self.env.user.student_id_computed.id

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Enviar respuesta',
            'res_model': 'faculty.response_exam_wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context':context,
            'target': 'new',
        }
        return action



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

    state = field_name = fields.Selection([
        ('submitted', 'Enviada'),
        ('qualified','Calificada')
    ], string='Estado', default="submitted")

    file_response = fields.Binary(string='Adjunto',required=True)
    filename = fields.Char()
    exam_id = fields.Many2one('faculty.exam', string='Examen')
    student_id = fields.Many2one('faculty.student', string='Estudiante')
    response_description = fields.Text(string='Descripcion')
    mark = fields.Float(string='Nota', digits=(5,2))
    comments = fields.Text(string='Comentarios')

    @api.multi
    def action_qualify_exam(self):

        action = {
            'type': 'ir.actions.act_window',
            'name': 'Enviar respuesta',
            'res_model': 'faculty.qualify_exam_wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context':{'response_id':self.id},
            'target': 'new',
        }
        return action