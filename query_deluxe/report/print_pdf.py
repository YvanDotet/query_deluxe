from odoo import models, fields, api


class PrintPdfParser(models.AbstractModel):
    _name = 'report.query_deluxe.pdf'
    _description = 'Parser for my pdf result'

    @api.model
    def get_report_values(self, docids, data=None):

        return {
            'query_name': data.get('query_name'),
            'headers': data.get('headers'),
            'bodies': data.get('bodies'),
        }
