from odoo import api, fields, models


class ProductsList(models.Model):
    _name = 'ocirestore.productslist'
    _description = 'New Description'

    name = fields.Selection(string='Categories', selection=[(
        'monitor', 'Monitor'), ('keyboard', 'Keyboard'), ('mouse', 'Mouse'), ('gpu', 'GPU'), ('cpu', 'CPU'), ('headset', 'Headset'), ('mousepad', 'Mousepad'), ('ram', 'RAM'), ])
    categories_id = fields.Char(string='Categories ID')
    products_ids = fields.One2many(
        comodel_name='ocirestore.products', inverse_name='products_id', string='Products')
    lists = fields.Char(string='Lists')

    total_products = fields.Char(
        compute='_compute_total_products', string='Total Products')

    _sql_constraints = [
        ('unique_category', 'unique (name)', 'Category is already created!')
    ]
    
    @api.depends('products_ids')
    def _compute_total_products(self):
        for rec in self:
            product = self.env['ocirestore.products'].search(
                [('products_id', '=', rec.id)]).mapped('name')
            total = len(product)
            rec.total_products = total
            rec.lists = product

    @api.onchange('name')
    def _onchange_products_ids(self):
        if (self.name == 'monitor'):
            self.categories_id = 'mo1'
        elif (self.name == 'keyboard'):
            self.categories_id = 'key1'
        elif (self.name == 'mouse'):
            self.categories_id = 'ms1'
        elif (self.name == 'gpu'):
            self.categories_id = 'gp1'
        elif (self.name == 'cpu'):
            self.categories_id = 'cp1'
        elif (self.name == 'headset'):
            self.categories_id = 'hea1'
        elif (self.name == 'mousepad'):
            self.categories_id = 'mp1'
        elif (self.name == 'ram'):
            self.categories_id = 'ra1'
