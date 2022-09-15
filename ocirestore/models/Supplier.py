from odoo import api, fields, models


class Supplier(models.Model):
  _name = 'ocirestore.supplier'
  _description = 'New Description'

  name = fields.Char(string='Name')
  address = fields.Char(string='Address')
  phone_number = fields.Char(string='Phone Number')
  products_id = fields.Many2many(comodel_name='ocirestore.products', string='Products')

  _sql_constraints = [
      ('unique_company', 'unique (name)', 'Company already on supplied!')
  ]
  
  