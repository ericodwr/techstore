from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_ceo = fields.Boolean(string='CEO')
    is_coo = fields.Boolean(string='COO')
    is_cfo = fields.Boolean(string='CFO')
    is_cto = fields.Boolean(string='CTO')
    is_cmo = fields.Boolean(string='CMO')

    is_membership = fields.Boolean(string='Membership')
    poin = fields.Integer(
        string='Poin', domain="[('is_membership', '=', True)]")
