from odoo import models, fields, api


class PrintPdfParser(models.AbstractModel):
    _name = 'report.query_deluxe.pdf'
    _description = 'Parser for my pdf result'

    @api.model
    def _get_report_values(self, docids, data=None):
        # append more informations to data
        print(docids)
        print(data)

        return {

        }
