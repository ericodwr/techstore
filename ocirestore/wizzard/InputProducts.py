from odoo import api, fields, models


class InputProducts(models.TransientModel):
    _name = 'ocirestore.inputproducts'

    product_id = fields.Many2one(
        comodel_name='ocirestore.products', string='Categories')
    add_stock = fields.Integer(string='Add Stock')

    # stock = fields.Integer(string='Stock', required=True)
    # sell_price = fields.Integer(string='Sell Price', required=True)
    # buy_price = fields.Integer(string='Buy Price', required=True)
    # supplier_id = fields.Many2many(
    #     comodel_name='ocirestore.supplier', string='Supplier')

    def button_inputproducts(self):
        for rec in self:
            self.env['ocirestore.products'].search([('id', '=', rec.product_id.id)]).write({
                'stock': rec.product_id.stock + rec.add_stock})
