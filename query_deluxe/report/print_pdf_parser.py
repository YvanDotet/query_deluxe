from odoo import fields, api, models


class PrintPdfParser(models.AbstractModel):
    _name = 'report.query_deluxe.pdf_layout'
    _description = 'Print pdf parser'

    def _get_datas(self, doc):
        headers, bodies = self.env['querydeluxe']._get_result_from_query(doc.name)
        return headers, bodies

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': self.env['querydeluxe'].browse(docids),
            'doc_model': 'querydeluxe',
            'data': data,
            'get_datas': self._get_datas
        }
