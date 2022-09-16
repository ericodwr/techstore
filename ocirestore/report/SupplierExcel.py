from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.ocirestore.report_supplier_xlsx'
    _description = 'Ya'
    _inherit = 'report.report_xlsx.abstract'
    date_report = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, supplier):
        sheet = workbook.add_worksheet('Supplier List')
        bold = workbook.add_format({'bold': True})
        sheet.write(1, 0, str(self.date_report))
        sheet.write(2, 0, 'Brand', bold)
        sheet.write(2, 1, 'Address', bold)
        sheet.write(2, 2, 'Phone Number', bold)
        sheet.write(2, 3, 'Products', bold)
        col = 3
        row = 0

        for obj in supplier:
            sheet.write(col, row, obj.name)
            sheet.write(col, row + 1, obj.address)
            sheet.write(col, row + 2, obj.phone_number)
            for product in obj.products_id:
                sheet.write(col, row + 3, product.name)
                col += 1
            col += 1
