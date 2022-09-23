from odoo import api, fields, models


class TransactionReport(models.TransientModel):
    _name = 'ocirestore.transactionreport'
    _description = 'New Description'

    name = fields.Char(string='Name')
    membership_id = fields.Many2one(
        comodel_name='res.partner', string='Membership ID')
    from_date = fields.Date(string='From Date', required=False)
    to_date = fields.Date(string='To Date', required=False)

    def action_transaction_report(self):
        filter = []
        membership_id = self.membership_id
        if membership_id:
            filter += [('membership_id', '=', membership_id.id)]
        transaction = self.env['ocirestore.transaction'].search([])
        data = {
            'form': self.read()[0],
            'transactional': transaction
        }
        # print(data)
        return self.env.ref('ocirestore.wizzard_transaction_report_pdf').report_action(self, data=data)
