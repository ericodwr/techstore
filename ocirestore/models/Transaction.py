from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Transaction(models.Model):
    _name = 'ocirestore.transaction'
    _description = 'New Description'

    name = fields.Char(string='No. Nota')
    client = fields.Many2one(string='Name Client', comodel_name='res.partner')
    transaction_date = fields.Datetime('Date', default=fields.Datetime.now())
    total_pay = fields.Integer(
        compute='_compute_total_pay', string='Total Pay')
    total_qty = fields.Integer(
        compute='_compute_total_qty', string='Total Quantity')
    transaction_ids = fields.One2many(
        comodel_name='ocirestore.detailtransaction', inverse_name='transaction_id', string='Transactions')

    state = fields.Selection(string='State', selection=[(
        'draft', 'Draft'), ('confirm', 'confirm'), ('done', 'Done'), ('cancel', 'Cancelled'), ], required=True, readonly=True, default='draft')

    # state

    def action_confirm(self):
        self.write({
            'state': 'confirm'
        })

    def action_done(self):
        self.write({
            'state': 'done'
        })

    def action_cancel(self):
        self.write({
            'state': 'cancel'
        })

    def action_draft(self):
        self.write({
            'state': 'draft'
        })

    # Constraints
    _sql_constraints = [
        ('unique_nota_num', 'unique (name)', 'Nota is already used!')
    ]

    # CRUD

    # Edit transaction
    def write(self, vals):
        for rec in self:
            data = self.env['ocirestore.detailtransaction'].search(
                [('transaction_id', '=', rec.id)])
            for early_data in data:
                early_data.products_id.stock += early_data.qty
        record = super(Transaction, self).write(vals)
        new_data = self.env['ocirestore.detailtransaction'].search(
            [('transaction_id', '=', rec.id)])
        for data in new_data:
            if data in new_data:
                data.products_id.stock -= data.qty
            else:
                pass
        return record

    # Delete Transaction (Odoo 15)
    # @api.ondelete(at_uninstall=False)
    # def _ondelete_transaction(self):
    #     if self.transaction_ids:
    #         data = []
    #         for rec in self:
    #             data = self.env['ocirestore.detailtransaction'].search(
    #                 [('transaction_id', '=', rec.id)])

    #         for newdata in data:
    #             newdata.products_id.stock += newdata.qty

    # Delete Transaction (Odoo < 15)
    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError(
                'Only can delete the transaction if state status is "Draft"!')
        else:
            if self.transaction_ids:
                data = []
                for rec in self:
                    data = self.env['ocirestore.detailtransaction'].search(
                        [('transaction_id', '=', rec.id)])
                for newData in data:
                    newData.products_id.stock += newData.qty

        return super().unlink()

    # Count total price

    @api.depends('transaction_ids')
    def _compute_total_pay(self):
        for rec in self:
            total = sum(self.env['ocirestore.detailtransaction'].search(
                [('transaction_id', '=', rec.id)]).mapped('total_price'))
            rec.total_pay = total

    # Total Quantity
    @api.depends('transaction_ids')
    def _compute_total_qty(self):
        for rec in self:
            total = sum(self.env['ocirestore.detailtransaction'].search(
                [('transaction_id', '=', rec.id)]).mapped('qty'))
            rec.total_qty = total


class DetailTransaction(models.Model):
    _name = 'ocirestore.detailtransaction'
    _description = 'New Description'

    name = fields.Char(string='Name')
    transaction_id = fields.Many2one(
        'ocirestore.transaction', string='Transaction Detail')
    products_id = fields.Many2one(
        comodel_name='ocirestore.products', string='Products')
    price = fields.Integer(string='Price')
    qty = fields.Integer(string='Quantity')
    total_price = fields.Integer(
        compute='_compute_total_price', string='Total Price')

    # Counting Total Price
    @api.depends('price', 'qty')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.price * rec.qty

    # Constraints for Quantity
    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty < 1:
                raise ValidationError(
                    f'Minimum quantity transaction for {rec.products_id.name} is 1.')
            elif (rec.products_id.stock < rec.qty):
                raise ValidationError(
                    f'Sorry, your quantity request is exceed our stock which is {rec.products_id.stock}')

    # Adding product's price
    @api.onchange('products_id')
    def _onchange_products_id(self):
        if (self.products_id.sell_price):
            self.price = self.products_id.sell_price

    # Create Transaction and remove the quantity of product

    @api.model
    def create(self, vals_list):
        record = super(DetailTransaction, self).create(vals_list)
        if record.qty:
            self.env['ocirestore.products'].search([('id', '=', record.products_id.id)]).write({
                'stock': record.products_id.stock - record.qty
            })
            return record
