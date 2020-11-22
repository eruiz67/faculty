# -*- coding: utf-8 -*-
from odoo import http

# class Faculty(http.Controller):
#     @http.route('/faculty/faculty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/faculty/faculty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('faculty.listing', {
#             'root': '/faculty/faculty',
#             'objects': http.request.env['faculty.faculty'].search([]),
#         })

#     @http.route('/faculty/faculty/objects/<model("faculty.faculty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('faculty.object', {
#             'object': obj
#         })