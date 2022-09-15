from odoo import api, fields, models


class Products(models.Model):
    _name = 'ocirestore.products'
    _description = 'New Description'

    name = fields.Char(string='Name')
    products_id = fields.Many2one(
        comodel_name='ocirestore.productslist', string='Categories')
    stock = fields.Integer(string='Stock', required=True)
    sell_price = fields.Integer(string='Sell Price', required=True)
    buy_price = fields.Integer(string='Buy Price', required=True)
    supplier_id = fields.Many2many(comodel_name='ocirestore.supplier', string='Supplier')
    
    _sql_constraints = [
        ('unique_product', 'unique (name)', 'Product already on list!')
    ]
