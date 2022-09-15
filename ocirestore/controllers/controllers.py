# -*- coding: utf-8 -*-
# from odoo import http


# class Ocirestore(http.Controller):
#     @http.route('/ocirestore/ocirestore', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ocirestore/ocirestore/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ocirestore.listing', {
#             'root': '/ocirestore/ocirestore',
#             'objects': http.request.env['ocirestore.ocirestore'].search([]),
#         })

#     @http.route('/ocirestore/ocirestore/objects/<model("ocirestore.ocirestore"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ocirestore.object', {
#             'object': obj
#         })
