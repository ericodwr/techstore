from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.ocirestore.report_transaction_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    date_report = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, transaction):
        sheet = workbook.add_worksheet('transaction List')
        bold = workbook.add_format({'bold': True})
        sheet.write(1, 0, str(self.date_report))
        sheet.write(2, 0, 'No. Nota', bold)
        sheet.write(2, 1, 'Name', bold)
        sheet.write(2, 2, 'Datetime', bold)
        sheet.write(2, 3, 'Products', bold)
        sheet.write(2, 4, 'Price', bold)
        sheet.write(2, 5, 'Quantity', bold)
        sheet.write(2, 6, 'Total Price', bold)
        col = 3
        row = 0

        for obj in transaction:
            sheet.write(col, row, obj.name)
            sheet.write(col, row + 1, obj.client)
            sheet.write(col, row + 2, str(obj.transaction_date))
            for product in obj.transaction_ids:
                sheet.write(col, row + 3, product.products_id.name)
                sheet.write(col, row + 4, product.price)
                sheet.write(col, row + 5, product.qty)
                sheet.write(col, row + 6, product.total_price)
                col += 1
            col += 1
            sheet.write(col, row + 4, 'Total Transaction', bold)
            sheet.write(col, row + 5, obj.total_qty)
            sheet.write(col, row + 6, obj.total_pay)
            col += 2
